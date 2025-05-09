import requests
from bs4 import BeautifulSoup
import time
import random
# Removed retry import
import arxiv # Add arxiv import

# Consider adding headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def search_arxiv(query, limit=10):
    """Searches the arXiv API for a given query."""
    print(f"Searching arXiv for: '{query}' (limit: {limit})")
    search_results = []
    try:
        # Use the arxiv library's Search object
        search = arxiv.Search(
            query=query,
            max_results=limit,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = list(arxiv.Client().results(search)) # Use default client

        print(f"  Found {len(results)} results on arXiv for '{query}'.")

        for result in results:
            # Map arXiv fields to our standard format
            authors_list = [str(author) for author in result.authors]
            # Modify the pdf_url assignment:
            pdf_url_candidate = result.pdf_url
            if pdf_url_candidate is None and result.entry_id:
                # Attempt to construct PDF URL from entry_id
                pdf_url_candidate = result.entry_id.replace('/abs/', '/pdf/')
                # Basic check to ensure it looks like a PDF URL now
                if not pdf_url_candidate.lower().endswith('.pdf'):
                     print(f"Warning: Constructed PDF URL for '{result.title[:50]}...' does not end with .pdf: {pdf_url_candidate}. Setting to None.")
                     pdf_url_candidate = None # Set to None if construction failed or looks wrong

            paper_data = {
                'title': result.title.replace('\n', ' ').strip() if result.title else "N/A",
                'url': result.entry_id, # Use entry_id as the primary URL for arXiv
                'pdf_url': pdf_url_candidate, # Use the candidate URL
                'authors_info': ", ".join(authors_list),
                'snippet': result.summary.replace('\n', ' ').strip() if result.summary else "N/A",
                'published_date': str(result.published.date()) if result.published else "N/A",
                'source_query': query,
                'source': 'arxiv' # Add source identifier
              }
            search_results.append(paper_data)
            print(f"    - arXiv: {paper_data['title'][:60]}...")
    except Exception as e:
        print(f"An error occurred during arXiv search for '{query}': {e}")

    # Add a small delay to be polite to the API
    time.sleep(random.uniform(1, 2))
    return search_results

# Removed retry decorator
def search_google_scholar(query, limit=10):
    """Searches Google Scholar for a given query and returns results."""
    print(f"Searching Google Scholar for: '{query}' (limit: {limit})")
    results = []
    # Basic URL encoding for the query
    query_encoded = requests.utils.quote(query)
    # Construct Google Scholar search URL (adjust domain if needed)
    url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={query_encoded}&btnG="

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find result containers (this selector might need adjustment based on Scholar's current HTML)
        paper_divs = soup.find_all('div', class_='gs_r gs_or gs_scl')

        for i, paper_div in enumerate(paper_divs):
            if i >= limit:
                break

            title_tag = paper_div.find('h3', class_='gs_rt')
            link_tag = title_tag.find('a') if title_tag else None
            pdf_link_tag = paper_div.find('div', class_='gs_ggsd') # Check for direct PDF links

            title = title_tag.text if title_tag else "N/A"
            url = link_tag['href'] if link_tag else "N/A"
            pdf_url = pdf_link_tag.find('a')['href'] if pdf_link_tag and pdf_link_tag.find('a') else None

            # Extract authors, publication info, abstract snippet (selectors might need updates)
            authors_div = paper_div.find('div', class_='gs_a')
            authors_info = authors_div.text if authors_div else "N/A"

            snippet_div = paper_div.find('div', class_='gs_rs')
            snippet = snippet_div.text if snippet_div else "N/A"

            paper_data = {
                'title': title,
                'url': url,
                'pdf_url': pdf_url, # Direct PDF link if found
                'authors_info': authors_info,
                'snippet': snippet,
                'source_query': query # Keep track of which query found this
            }
            results.append(paper_data)
            print(f"  Found: {title[:60]}...")

        # Add a small delay to avoid overwhelming the server
        time.sleep(random.uniform(1, 3)) # Restore shorter sleep

    except requests.exceptions.RequestException as e:
        # Simplified error handling
        print(f"Error during Google Scholar request for '{query}': {e}")
        return [] # Return empty list on error
    except Exception as e:
        print(f"An unexpected error occurred during scraping for '{query}': {e}")
        return [] # Also return empty list on other unexpected errors

    print(f"Found {len(results)} results for '{query}'.")
    return results

def find_papers(keyword_dict, search_limits):
    """Iterates through keyword categories and searches for papers using category-specific limits."""
    all_papers = {'high': [], 'medium': [], 'low': []}
    if not keyword_dict:
        print("No keywords provided for searching.")
        return all_papers

    seen_titles = set() # Initialize set to track titles for deduplication

    for category, keywords in keyword_dict.items():
        print(f"\n--- Searching category: {category} ---")
        if not keywords:
            print(f"No keywords in category '{category}'.")
            continue

        # Get the search limit for this specific category, default to 5 if not found
        limit_for_category = search_limits.get(category, 5)
        print(f"Using search limit for '{category}': {limit_for_category}") # Added print for clarity

        for keyword in keywords:
            # Existing call
            scholar_papers = search_google_scholar(keyword, limit=limit_for_category)
            # New call
            arxiv_papers = search_arxiv(keyword, limit=limit_for_category) # Use same limit for now

            # Combine results
            combined_papers = scholar_papers + arxiv_papers

            # Deduplicate and add category
            unique_papers_for_keyword = []
            for paper in combined_papers:
                normalized_title = paper.get('title', '').lower().strip()
                if normalized_title and normalized_title not in seen_titles:
                    paper['likelihood_category'] = category # Add category info
                    unique_papers_for_keyword.append(paper)
                    seen_titles.add(normalized_title)

            # Extend the main list with unique papers for this keyword
            all_papers[category].extend(unique_papers_for_keyword)

            # Add sleep between keywords
            sleep_duration = random.uniform(2, 5) # Shorter sleep between keywords now
            print(f"Sleeping for {sleep_duration:.2f} seconds before next keyword...")
            time.sleep(sleep_duration)

    return all_papers