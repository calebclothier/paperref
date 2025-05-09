
def format_title(title):
    """
    Format a paper title to remove \n and \r characters.
    """
    if not title:
        return ""
    return title.replace("\n", " ").replace("\r", "")

def format_author(author):
    """Helper function to format a single author name."""
    parts = author.split()
    if len(parts) > 1:
        return f"{parts[0][0]}. {parts[-1]}"
    return author


def get_first_author(authors_list):
    """Get the formatted first author."""
    if not authors_list:
        return ""
    return format_author(authors_list[0])


def get_last_author(authors_list):
    """Get the formatted last author."""
    if not authors_list:
        return ""
    if len(authors_list) > 1:
        return format_author(authors_list[-1])
    return ""


def format_authors(authors_list):
    """
    Format a list of authors to show first and last author with ellipsis for papers with more than two authors.
    
    Args:
        authors_list (list): List of author names
        
    Returns:
        str: Formatted author string
    """
    if not authors_list:
        return ""
    
    if len(authors_list) > 2:
        # Show first and last author with ellipsis
        first_author = get_first_author(authors_list)
        last_author = get_last_author(authors_list)
        return f"{first_author}, ..., {last_author}"
    elif len(authors_list) == 2:
        # Show both authors
        return f"{get_first_author(authors_list)}, {get_last_author(authors_list)}"
    else:
        # Show single author
        return get_first_author(authors_list)


def get_best_link(paper):
    """
    Get the best available link for a paper based on precedence:
    1. ArXiv PDF
    2. Open Access PDF
    
    Args:
        paper (dict): Paper data
        
    Returns:
        str: Best available link URL or None
    """
    if paper.get('arxiv'):
        return f"https://arxiv.org/pdf/{paper['arxiv']}"
    elif paper.get('open_access_url'):
        return paper['open_access_url']
    return None
