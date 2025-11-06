import requests
from requests.exceptions import RequestException
from minsearch import AppendableIndex
from typing import List, Dict, Any, Optional

index = AppendableIndex(text_fields=['summary'])

def get_page(url: str) -> str:
    """
    Get the Markdown content of a web page using the Jina Reader service.

    This function prepends the Jina Reader proxy URL to the provided `url`,
    sends a GET request with a timeout, and decodes the response as UTF-8 text.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        Optional[str]: The Markdown-formatted content of the page if the request
        succeeds; otherwise, None.

    Raises:
        None: All network or decoding errors are caught and suppressed.
               Logs or error messages could be added as needed.
    """
    jina_reader_base_url = 'https://r.jina.ai/'
    jina_reader_url = jina_reader_base_url + url

    try:
        response = requests.get(jina_reader_url, timeout=10)
        response.raise_for_status()
    except RequestException as e:
        raise ValueError(f"Failed to fetch URL '{url}': {e}") from e

    try:
        return response.content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Failed to decode response content for URL '{url}': {e}") from e

def search(query: str) -> List[Dict[str, Any]]:
    """
    Search the index for documents matching a query string.

    Args:
        query (str): The search query.

    Returns:
        List[Dict[str, Any]]: A list of search result dictionaries.
    """
    return index.search(query, num_results=5)

def save_summary(url: str, summary: Optional[str] = None) -> str:
    """
    Save the summary of a url

    Args:
        url (str): link to the web page.
        summary (str): summary of the web page contents

    Returns:
        str: "SUCCESS" upon successful indexing.
    """
    doc = {
        "url": url,
        "summary": summary
    }
    index.append(doc)

    return "SUCCESS"