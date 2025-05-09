import json
import os
import google.generativeai as genai
import sys # Added for sys.exit
from dotenv import load_dotenv # Added for .env loading
from paper_finder import find_papers
from paper_downloader import download_papers_from_results, download_file # Added import

def configure_gemini():
    """Configures the Gemini API with the key from environment variables."""
    load_dotenv() # Load environment variables from .env file
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set the GOOGLE_API_KEY environment variable with your API key.")
        return False
    try:
        genai.configure(api_key=api_key)
        print("Gemini API configured successfully.")
        return True
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return False

def generate_keywords_with_gemini(question):
    """Generates categorized search keywords using the Gemini API."""
    prompt = f"""
Analyze the following research question:
"{question}"

Generate a list of search keywords and terms relevant to this question.
Categorize these keywords into three levels of likelihood for finding relevant papers: 'high', 'medium', and 'low'.

Return the result *strictly* as a JSON string with the following structure:
{{"high": ["term1", "term2"], "medium": ["term3", "term4"], "low": ["term5"]}}

Ensure *only* the JSON string is present in your response, with no other text before or after it.
"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Clean the response text to ensure it's just the JSON
        # Sometimes models add backticks or 'json' prefix
        cleaned_response = response.text.strip().strip('```json').strip('```').strip()

        print(f"Raw Gemini Response:\n---\n{response.text}\n---") # Log raw response for debugging
        print(f"Cleaned Gemini Response:\n---\n{cleaned_response}\n---") # Log cleaned response

        keywords_dict = json.loads(cleaned_response)
        # Basic validation
        if not isinstance(keywords_dict, dict) or not all(k in keywords_dict for k in ['high', 'medium', 'low']):
             print("Error: Gemini response JSON structure is invalid.")
             return None
        if not all(isinstance(v, list) for v in keywords_dict.values()):
            print("Error: Gemini response JSON values are not all lists.")
            return None

        print("Successfully parsed keywords from Gemini response.")
        return keywords_dict
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from Gemini response.")
        print(f"Received: {cleaned_response}")
        return None
    except Exception as e:
        print(f"An error occurred during Gemini API call or processing: {e}")
        return None


def load_config(filepath="research_config.json"):
    """Loads the research configuration from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"Configuration loaded successfully from {filepath}")
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading config: {e}")
        return None

def save_overview_json(metadata_list, project_output_dir):
    """Saves the list of downloaded paper metadata to a JSON file."""
    try:
        # Construct the output filepath relative to project_output_dir
        filepath = os.path.join(project_output_dir, "overview.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved overview to {filepath}")
    except IOError as e:
        print(f"Error writing overview file {filepath}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving overview: {e}")


def main():
    """Main function to run the research process."""
    print("Starting literary research AI...")

    # Configure Gemini API first
    if not configure_gemini():
        sys.exit(1) # Exit if Gemini configuration fails

    config = load_config()
# --- Project Setup from Config ---
    if config: # Check if config loaded successfully
        subject_name = config.get("subject_name", "default_subject")
        # Basic validation for subject_name (replace invalid chars if needed, or just use as is for now)
        # For simplicity, we'll assume the user provides a valid name for now.
        # More robust validation could be added here.
        if not subject_name: # Handle empty string case
            print("Warning: 'subject_name' in config is empty, using 'default_subject'.")
            subject_name = "default_subject"

        search_limits = config.get("search_limits", {"high": 5, "medium": 3, "low": 2})
        # Basic validation for search_limits
        if not isinstance(search_limits, dict) or not all(k in search_limits for k in ['high', 'medium', 'low']):
            print("Warning: 'search_limits' structure in config is invalid or incomplete. Using defaults.")
            search_limits = {"high": 5, "medium": 3, "low": 2}
        if not all(isinstance(v, int) and v >= 0 for v in search_limits.values()):
             print("Warning: 'search_limits' values must be non-negative integers. Using defaults.")
             search_limits = {"high": 5, "medium": 3, "low": 2}

        print(f"Using Subject Name: {subject_name}")
        print(f"Using Search Limits: {search_limits}")

        base_output_dir = "research_outputs"
        try:
            os.makedirs(base_output_dir, exist_ok=True)
            project_output_dir = os.path.join(base_output_dir, subject_name)
            os.makedirs(project_output_dir, exist_ok=True)
            print(f"Using Project Output Directory: {project_output_dir}")
        except OSError as e:
            print(f"Error creating output directories: {e}")
            # Decide how to handle this - exit or continue with default? For now, let's exit.
            sys.exit(f"Failed to create necessary output directories: {e}")
        except Exception as e:
             print(f"An unexpected error occurred during output directory creation: {e}")
             sys.exit(f"Unexpected error during output directory creation: {e}")

    else: # Handle case where config failed to load earlier
        print("Configuration could not be loaded. Cannot proceed with project setup.")
        sys.exit(1) # Exit if config is None
    # --- End Project Setup ---

    if config and "research_question" in config:
        question = config["research_question"]
        print(f"\nLoaded Research Question: {question}")

        # Generate keywords using Gemini
        print("\nGenerating keywords with Gemini...")
        keywords = generate_keywords_with_gemini(question)

        if keywords:
            print("\nGenerated Keywords:")
            print(json.dumps(keywords, indent=2))
            # Search for papers using the generated keywords
            print("\nSearching for papers using keywords...")
            # You can adjust results_per_keyword here if needed
            found_papers = find_papers(keywords, search_limits) # Pass the loaded search limits

            print("\n--- Paper Search Results ---")
            if found_papers:
                for category, papers in found_papers.items():
                    print(f"Category '{category}': Found {len(papers)} papers.")
                # Optional: Print more details if needed
                # print("\nDetailed Found Papers:")
                # print(json.dumps(found_papers, indent=2))
            else:
                print("No papers found or an error occurred during search.")
            print("--- End Paper Search Results ---")

            # --- Download Papers ---
            print("\nAttempting to download found papers...")
            downloaded_metadata = download_papers_from_results(found_papers, project_output_dir, search_limits)
            if downloaded_metadata:
                print(f"\nSuccessfully downloaded {len(downloaded_metadata)} papers.")
                # Save the overview JSON
                save_overview_json(downloaded_metadata, project_output_dir)
                # Optional: Save or process downloaded_metadata if needed later
                # with open("downloaded_papers_metadata.json", "w", encoding="utf-8") as f:
                #     json.dump(downloaded_metadata, f, indent=2)
            else:
                print("\nNo papers were successfully downloaded.")
            # --- End Download Papers ---

        else:
            print("\nFailed to generate keywords using Gemini.")

    else:
        print("Could not load research question from config. Exiting.")

if __name__ == "__main__":
    main()