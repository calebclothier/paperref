"""Recommended paper services for generating a user's recommended papers list based on a list of user input papers."""

import os
import requests
from fastapi import HTTPException

from app.config import settings
from app.schemas.papers import Paper
from app.utils.paper import parse_paper_detail
from app.services.graph import get_references_service, get_citations_service

# from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors.rankllm_rerank import RankLLMRerank


def get_paper_recommendations_service(user_papers: list[Paper]) -> list[Paper]:
    """
    Generates a list of recommended papers based on an input list of user papers.

    Args:
        user_papers (list[Paper]): List of user papers

    Returns:
        list[Paper]: List of recommended papers

    Raises:
        HTTPException: Raises any exception during recommendation fetching
    """
    return get_custom_recommendations(user_papers)

        
def get_semantic_scholar_recommendations(user_papers: list[Paper]):
    paper_ids = [paper.id for paper in user_papers]
    payload = {"positivePaperIds": paper_ids, "negativePaperIds": []}
    base_url = "https://api.semanticscholar.org/recommendations/v1/papers"
    fields = ["title", "authors", "year", "publicationDate", "url", "citationCount"]
    full_url = base_url + "?fields=" + ",".join(fields)
    try:
        response = requests.post(
            url=full_url,
            headers={"content-type": "application/json; charset=UTF-8"},
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        response = response.json()
        papers = response["recommendedPapers"]
        return [Paper(**parse_paper_detail(paper)) for paper in papers]
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching recommendations: {e}"
        )
        
        
def get_custom_recommendations(user_papers: list[Paper]):
    
    # Set the OPENAI_API_KEY environment variable
    # TODO: Find a better way to set the API key
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    
    # Generate candidate recommendations
    ss_recommendations = get_semantic_scholar_recommendations(user_papers)
    references = get_references_service(user_papers)
    citations = get_citations_service(user_papers)
    
    # Combine all recommendations
    seen = set()
    user_paper_ids = set(paper.id for paper in user_papers)
    all_recommendations = []
    for paper in [*ss_recommendations, *references, *citations]:
        if paper.id not in user_paper_ids and paper.id not in seen:
            all_recommendations.append(paper)
            seen.add(paper.id)
    papers_dict = {paper.id: paper for paper in all_recommendations}
    
    # Create a vector store
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    documents = [
        Document(
            page_content=" ".join([paper.title or "", paper.abstract or ""]),
            metadata={
                "paper_id": paper.id,
                "citations": paper.citation_count,
            }
        ) for paper in all_recommendations]
    
    # Create a retriever
    retriever = FAISS.from_documents(documents, embedding).as_retriever(search_kwargs={"k": 50})
    
    # Add reranking to the retriever
    compressor = RankLLMRerank(top_n=10, model="gpt", gpt_model="gpt-4o-mini")
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
    
    # Generate a summary of the user's paper library
    llm = ChatOpenAI(model="gpt-4o")
    paper_details = [f"{paper.title or ''}\n{paper.abstract or ''}" for paper in user_papers]
    prompt = "Summarize the following paper library in 1-2 paragraphs:\n\n" + "\n\n".join(paper_details)
    summary = llm.invoke(prompt)
    
    # Retrieve relevant papers
    results = compression_retriever.get_relevant_documents(summary.content)
    
    # Return the top 10 results
    return [papers_dict[paper.metadata["paper_id"]] for paper in results]