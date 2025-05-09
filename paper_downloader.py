import requests
import os
import time
import random
import re
from urllib.parse import urlparse

# Re-use headers from paper_finder
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def sanitize_filename(filename):
    """Removes or replaces characters invalid for filenames."""
    # Remove invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    # Replace spaces with underscores (optional, but common)
    sanitized = sanitized.replace(" ", "_")
    # Limit length (optional)
    return sanitized[:150] # Limit to 150 chars to be safe

def download_file(paper_info, project_output_dir):
    """Attempts to download a file for a given paper_info dictionary."""
    title = paper_info.get('title', 'untitled_paper')
    download_url = paper_info.get('pdf_url') # Use pdf_url as the primary download URL
    source_url = paper_info.get('url') # Fallback or alternative source
    category = paper_info.get('likelihood_category', 'unknown')

    # Determine target directory
    # Store files in a general 'downloads' directory within the category
    target_dir = os.path.join(project_output_dir, "downloads", category)
    os.makedirs(target_dir, exist_ok=True)

    # Create a sanitized filename base
    filename_base = sanitize_filename(title)

    if not download_url:
        print(f"No download URL found for '{title[:50]}...'. Cannot download.")
        return None

    # --- Trial and Verify Extensions (.pdf, .doc) ---
    extensions_to_try = ['.pdf', '.doc']
    successful_download = False
    filepath = None

    for ext in extensions_to_try:
        filepath = os.path.join(target_dir, f"{filename_base}{ext}")
        print(f"Attempting to download '{title[:50]}...' with extension '{ext}' from {download_url}")

        try:
            # Add a small random delay
            time.sleep(random.uniform(0.5, 1.5))
            response = requests.get(download_url, headers=HEADERS, stream=True, timeout=30) # Added timeout
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # If we reach here, the download was successful for this extension
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded and saved: {filepath}")
            successful_download = True
            break # Stop trying extensions if one is successful

        except requests.exceptions.Timeout:
            print(f"Timeout occurred while downloading '{title[:50]}...' with extension '{ext}' from {download_url}")
            # Continue to next extension if timeout occurs
            continue
        except requests.exceptions.RequestException as e:
            # This includes 404 errors, which means the file with this extension wasn't found
            print(f"Download failed for '{title[:50]}...' with extension '{ext}' from {download_url}: {e}")
            # Continue to next extension
            continue
        except Exception as e:
            print(f"An unexpected error occurred during download/saving for '{title[:50]}...' with extension '{ext}': {e}")
            # Continue to next extension
            continue

    if successful_download:
        paper_info['downloaded_filepath'] = filepath # Add filepath to dict
        return paper_info # Return updated info on success
    else:
        print(f"Failed to download '{title[:50]}...' after trying all extensions.")
        return None


def download_papers_from_results(found_papers, project_output_dir, search_limits):
    """Iterates through found papers and attempts to download files, enforcing a total limit."""
    downloaded_papers_metadata = []
    if not found_papers:
        print("No papers found to download.")
        return downloaded_papers_metadata

    # Calculate the total desired limit from search_limits
    total_limit = sum(search_limits.values())
    print(f"\n--- Attempting to download papers (Total Limit: {total_limit}) ---")

    download_count = 0
    for category, papers in found_papers.items():
        print(f"\n-- Processing category: {category} ({len(papers)} papers) --")
        for paper in papers:
            if download_count >= total_limit:
                print(f"Total download limit ({total_limit}) reached. Stopping download process.")
                return downloaded_papers_metadata # Stop and return early

            download_result = download_file(paper, project_output_dir) # paper dict is updated in-place on success
            if download_result:
                downloaded_papers_metadata.append(download_result)
                download_count += 1

    print(f"\n--- Download process completed. Successfully downloaded {download_count} papers. ---")
    return downloaded_papers_metadata