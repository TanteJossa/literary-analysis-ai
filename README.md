# Literary Research AI Automator

This Python project automates several key steps in the literary and academic research process. It leverages the Google Gemini API for advanced text analysis and keyword generation, searches for academic papers, and downloads them to streamline your research workflow.

## Project Overview

The core functionality of this project revolves around automating the initial phases of research paper gathering. It is designed to:

1.  **Configure API Access:** Securely configure the Google Gemini API using an API key stored in an `.env` file.
2.  **Load Research Parameters:** Read the main research question, a subject name for organizing outputs, and search limits from a central [`research_config.json`](research_config.json:0) file.
3.  **Generate Keywords:** Utilize the Gemini API ([`gemini-1.5-flash`](https://gemini.google.com/models/gemini-1.5-flash:0) as per [`main.py`](main.py:40)) to analyze the research question and generate a categorized list of search keywords (high, medium, low probability).
4.  **Find Academic Papers:** (Handled by the `paper_finder.py` module) Use the generated keywords to search for relevant academic papers.
5.  **Download Papers:** (Handled by the `paper_downloader.py` module) Download the papers found during the search phase.
6.  **Organize Outputs:** Save downloaded papers and an `overview.json` (containing metadata of downloaded papers) into a structured directory: `research_outputs/<subject_name>/`.

### Key Files and Modules

*   [`main.py`](main.py:1): The main script that orchestrates the entire automated research process.
*   `paper_finder.py`: A module responsible for searching for academic papers based on keywords. (Note: Functionality is inferred from its usage in [`main.py`](main.py:165)).
*   `paper_downloader.py`: A module responsible for downloading the identified academic papers. (Note: Functionality is inferred from its usage in [`main.py`](main.py:180)).
*   [`research_config.json`](research_config.json:0): A JSON configuration file to specify the research question, subject name, and limits for paper searching.
*   `.env`: An environment file to securely store the `GOOGLE_API_KEY`.
*   [`requirements.txt`](requirements.txt:0): Lists the necessary Python packages for the project.

## Features

*   **Gemini API Integration:** Seamlessly configures and uses the Google Gemini API ([`genai.configure()`](main.py:18), [`genai.GenerativeModel()`](main.py:40)) for intelligent text processing.
*   **Automated Keyword Generation:** Leverages Gemini ([`generate_keywords_with_gemini()`](main.py:25)) to produce categorized keywords ('high', 'medium', 'low' likelihood) tailored to your research question, enhancing search efficiency.
*   **Configurable Research:** Allows users to define research parameters (subject, question, search depth) via the [`research_config.json`](research_config.json:0) file ([`load_config()`](main.py:70)).
*   **Automated Paper Discovery:** Systematically finds academic papers relevant to your research using the `paper_finder.py` module.
*   **Automated Paper Downloading:** Downloads accessible papers using the `paper_downloader.py` module.
*   **Structured Output Management:** Organizes downloaded materials and metadata (`overview.json`) into project-specific folders under `research_outputs/` ([`save_overview_json()`](main.py:87), [`os.makedirs()`](main.py:134)).
*   **Robust Error Handling:** Includes checks and error messages for API configuration, file operations, and JSON parsing (e.g., in [`configure_gemini()`](main.py:9), [`load_config()`](main.py:70), [`generate_keywords_with_gemini()`](main.py:25)).

## Setup

### Prerequisites

*   Python 3.x
*   Access to the Google Gemini API and a valid API key.

### Installation Steps

1.  **Clone/Download:**
    Obtain the project files (e.g., by cloning the repository if it's hosted on a version control system, or by downloading the script files).

2.  **Install Dependencies:**
    Install the required Python libraries listed in [`requirements.txt`](requirements.txt:0). Typically, this includes:
    ```bash
    pip install google-generativeai python-dotenv
    ```
    (Note: `paper_finder.py` and `paper_downloader.py` might have additional dependencies not listed here. Ensure all necessary libraries for those modules are also installed.)

3.  **Configure Environment Variable:**
    *   Create a file named `.env` in the root directory of the project.
    *   Add your Google Gemini API key to this file:
        ```env
        GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
        ```
    This key is loaded by the [`load_dotenv()`](main.py:11) function.

4.  **Prepare Configuration File:**
    Create or update the [`research_config.json`](research_config.json:0) file in the project root. See the "Usage" section for an example structure.

## Usage

1.  **Define Your Research in `research_config.json`:**
    Modify the [`research_config.json`](research_config.json:0) file to specify your research parameters.
    Example:
    ```json
    {
      "subject_name": "AI_in_Healthcare_Diagnostics",
      "research_question": "How is artificial intelligence transforming diagnostic processes in modern healthcare?",
      "search_limits": {
        "high": 5,
        "medium": 3,
        "low": 2
      }
    }
    ```
    *   `subject_name`: A descriptive name for your research project (e.g., "AI_in_Healthcare"). This will be used to create a dedicated output directory.
    *   `research_question`: The central question guiding your research.
    *   `search_limits`: An object defining the maximum number of papers to attempt to download for each keyword category.

2.  **Run the Main Script:**
    Execute the [`main.py`](main.py:1) script from your terminal in the project's root directory:
    ```bash
    python main.py
    ```

3.  **Review Outputs:**
    *   The script will output progress information and any errors to the console.
    *   Downloaded papers and an `overview.json` file (listing metadata of successfully downloaded papers) will be located in the `research_outputs/<your_subject_name>/` directory.

## Research Workflow Integration

This project can be a valuable component of a broader, multi-step research workflow. Here's an example of how it might fit:

### Step 1: Locate Sources

*   **Initial Exploration & Manual Collection:**
    *   **x.com (formerly Twitter):** Utilize platforms like x.com, potentially with tools like Grok, for deep dives into current discussions, pre-prints, and expert opinions.
    *   **Google Gemini Deep Research:** Conduct direct, in-depth research using the capabilities of Google Gemini models.
    *   **Efficient Text Extraction:** A suggested method for capturing web content involves using browser developer tools to "Copy element." This HTML can then be processed by AI Studio (e.g., with Gemini 1.5 Pro) to accurately extract text and identify nearby source citations.
*   **Automated Paper Retrieval (This Project):**
    *   Use this "Literary Research AI Automator" (specifically its `paper_finder.py` and `paper_downloader.py` components, orchestrated by [`main.py`](main.py:1)) to systematically find and download academic papers. This is driven by the keywords generated from your [`research_config.json`](research_config.json:0).

### Step 2: Combine/Analyze Sources

*   **Synthesize Information:**
    *   Employ a powerful language model like Gemini 1.5 Pro to create a single, cohesive document. This document should integrate information from all collected sources (both manually and automatically gathered).
    *   **Crucially, ensure every statement or piece of information is meticulously attributed to its original source within this combined document.**

### Step 3: Execute Research and Create Graphs/Visualizations

*   **Define Methodology and Targets:**
    *   Use Gemini to help brainstorm and refine the research methodology, specific aims, and measurable targets for your study.
*   **Data Analysis and Visualization (Roocode Environment):**
    *   The term "Gemini in Roocode" refers to a development environment (likely VS Code or a similar IDE) enhanced with Gemini integration (e.g., through extensions or APIs) for coding tasks.
    *   **Graph Generation:** Within this "Roocode" environment, use Python (with libraries such as Matplotlib, Seaborn, Plotly) to process raw data and generate insightful graphs and visualizations.
    *   **File Organization:** Store the generated image files (graphs) in clearly structured folders.
    *   **Textual Summaries:** Also in "Roocode," generate JSON files containing textual summaries of the research results, complementing the visual data.

### Step 4: Summarize Result

*   **Comprehensive Summary:**
    *   Develop a final summary of your research findings. This summary should be deeply informed by the synthesized document created in Step 2, ensuring that all key insights are presented with supporting evidence from the collated sources.

### Step 5: Create TeX Report

*   **Formal Report Generation:**
    *   Produce a formal academic report using LaTeX. This involves creating a main `.tex` document for the report's structure and content.
    *   **Bibliography Management:** Utilize a `references.bib` file in conjunction with BibTeX or BibLaTeX to manage citations and automatically generate a formatted bibliography.
*   **Debugging (Roocode Debug):**
    *   The "Roocode debug" environment (again, likely referring to debugging capabilities within VS Code or a similar IDE, possibly with LaTeX-specific tools or extensions) is used to troubleshoot and resolve any issues in the `.tex` file, ensuring it compiles correctly and meets formatting requirements.

## Latex Download Tool Explanation

In the context of the research workflow described (particularly Step 5), a "latex download tool" would facilitate the setup for creating TeX reports. While this project's `paper_downloader.py` focuses on retrieving research papers (often as PDFs), a dedicated LaTeX download tool could serve several complementary functions:

*   **Downloading LaTeX Distributions:** These are complete TeX/LaTeX systems. A tool might automate the download and installation of distributions like MiKTeX (common on Windows), TeX Live (cross-platform), or MacTeX (for macOS). For example, `protext` is an easy installer for MiKTeX.
*   **Fetching LaTeX Templates:** Such a tool could download standard academic paper templates (e.g., from IEEE, ACM, Springer, Elsevier, or specific university repositories). This provides a pre-formatted structure for the `.tex` report.
*   **Downloading Papers as LaTeX Source:** Some academic archives, most notably arXiv.org, provide papers in their original LaTeX source format (often as `.tar.gz` or `.zip` files containing `.tex` files, images, `.bib` files, etc.). A specialized tool could prioritize or specifically fetch these source bundles when available.
*   **Relationship to `paper_downloader.py`:**
    *   Currently, `paper_downloader.py` (as inferred from [`main.py`](main.py:1)) is geared towards general file downloading based on search results.
    *   If `paper_downloader.py` were to be enhanced, it could potentially include functionality to detect and prefer LaTeX source versions of papers from repositories that offer them. However, as it stands, a separate "latex download tool" would likely focus on the broader LaTeX ecosystem (distributions, templates) rather than just individual paper sources.

In essence, a "latex download tool" streamlines acquiring the necessary LaTeX software, templates, or even paper source files, thereby preparing the environment for the TeX report creation phase of the research workflow.

## Contributing

(Details on how to contribute to this project can be added here, e.g., fork the repository, create a feature branch, submit a pull request.)

## License

(Specify the license for this project, e.g., MIT License. If a `LICENSE` file is present in the repository, refer to it.)
