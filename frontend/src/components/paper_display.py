"""Component for displaying paper details."""

import streamlit as st

from typing import Optional

from src.api.library import add_paper


def _render_paper_content(
    paper: dict,
    show_add_button: bool = False,
    on_add: Optional[callable] = None,
    show_remove_button: bool = False,
    on_remove: Optional[callable] = None,
    button_key: Optional[str] = None,
    link_columns: int = 5,  # Number of columns for links
    header_with_button: bool = True # Whether header includes a button column
) -> None:
    """Helper function to render the core paper content."""
    
    # Generate unique key for buttons based on paper DOI or provided key
    button_key = button_key or f"paper_{paper.get('doi', 'unknown')}"

    # Create columns for the header section if needed
    if header_with_button:
        header_col, button_col = st.columns([0.9, 0.1])
    else:
        header_col = st.container() # Use a container to keep indentation consistent
        

    with header_col:
        # Title
        st.markdown(f"#### {paper['title']}")
        
        # Authors
        if paper.get('authors'):
            st.markdown(", ".join(paper['authors']))
            
        # Journal and year
        if paper.get('journal'):
            st.markdown(f"{paper.get('year', '')}, _{paper['journal']}_")
        else:
            st.markdown(f"{paper.get('year', '')}")
        
        # Citation count
        if paper.get('citation_count'):
            st.markdown(f"{paper['citation_count']} citations")
    
    # Add button in header if configured
    if header_with_button and show_add_button and on_add:
        with button_col:
            st.button("", 
                icon=":material/add:",
                on_click=on_add,
                key=f"add_{button_key}", 
                use_container_width=True)
            
    # Links
    links = []
    if paper.get('arxiv'):
        links.extend([
            {
                "label": "",
                "icon": ":material/picture_as_pdf:",
                "url": f"https://arxiv.org/pdf/{paper['arxiv']}"
            },
            {
                "label": "**X**",
                "help": "ArXiv",
                "icon": None,
                "url": f"https://arxiv.org/abs/{paper['arxiv']}"
            }
        ])
    # if paper.get('open_access_url'):
    #     links.append({
    #         "label": "Open Access",
    #         "icon": ":material/picture_as_pdf:",
    #         "url": paper['open_access_url']
    #     })
    
    if links:
        cols = st.columns(link_columns)
        # Render each link in its own column
        for col, link in zip(cols, links):
            with col:
                st.link_button(
                    label=link["label"],
                    icon=link["icon"],
                    url=link["url"],
                    use_container_width=True
                )
    
    # TLDR
    if paper.get('tldr'):
        st.markdown(f"_TLDR_: {paper['tldr']}")
    
    # Abstract in expandable section
    if paper.get('abstract'):
        with st.expander("Abstract", expanded=False):
            st.markdown(paper['abstract'])
            
    # Remove button at the bottom if configured
    if not header_with_button and show_remove_button and on_remove:
        # st.divider()
        st.button("Remove from Library", 
            icon=":material/remove:",
            on_click=on_remove,
            key=f"remove_{button_key}", 
            use_container_width=True)



def display_paper(
    paper: Optional[dict],
    show_add_button: bool = False,
    on_add: Optional[callable] = None,
    button_key: Optional[str] = None,
    use_container: bool = True
) -> None:
    """
    Display paper details in an aesthetically pleasing container.
    Typically used for search results.
    
    Args:
        paper (Optional[dict]): The paper data to display, or None if no results
        show_add_button (bool): Whether to show the add to library button
        on_add (Optional[callable]): Callback function when add button is clicked
        button_key (Optional[str]): Optional key to use for button uniqueness
        use_container (bool): Whether to wrap the content in a bordered container.
    """
    if not paper:
        st.info("No paper data available.")
        return

    # Conditionally wrap content in a container
    if use_container:
        with st.container(border=True):
            _render_paper_content(
                paper=paper,
                show_add_button=show_add_button,
                on_add=on_add,
                button_key=button_key,
                link_columns=5, # Standalone uses 5 columns for links
                header_with_button=True
            )
    else:
        _render_paper_content(
            paper=paper,
            show_add_button=show_add_button,
            on_add=on_add,
            button_key=button_key,
            link_columns=5,
            header_with_button=True
        )
        

def display_paper_sidebar(
    paper: Optional[dict],
    on_remove: Optional[callable] = None,
    button_key: Optional[str] = None,
) -> None:
    """
    Display paper details specifically formatted for the sidebar.
    Includes a remove button at the bottom.
    
    Args:
        paper (Optional[dict]): The paper data to display, or None if no results
        on_remove (Optional[callable]): Callback function when remove button is clicked
        button_key (Optional[str]): Optional key to use for button uniqueness
    """
    if not paper:
        st.info("No paper data available.")
        return

    _render_paper_content(
        paper=paper,
        show_remove_button=True,
        on_remove=on_remove,
        button_key=button_key,
        link_columns=3, # Sidebar uses 3 columns for links
        header_with_button=False # Sidebar doesn't have button in header
    )