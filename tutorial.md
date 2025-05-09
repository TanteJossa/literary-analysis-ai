# My Research Paper Creation Workflow

This tutorial outlines the steps I follow to create my research papers.

## Step 1: Locate Sources

*   **x.com:** Use Grok for deep research on x.com.
*   **Gemini Deep Research:** Conduct in-depth research using Gemini.
    *   **Method:** Copy the relevant HTML element using browser developer options. Then, use AI Studio with Gemini 1.5 Pro to extract the text, ensuring that source citations are captured accurately and are in close proximity to the extracted text.
*   **Paper Download Tool:** Utilize the project's tool (referring to [`paper_downloader.py`](paper_downloader.py:1) from the main project) to download research papers.

## Step 2: Combine/Analyze

*   Use Gemini 1.5 Pro to create a single, comprehensive document that synthesizes all information from the gathered sources.
*   Crucially, ensure that every statement or piece of information within this document is attributed to its original source.

## Step 3: Execute Research and Create Graphs

*   **Methods and Targets:** Let Gemini assist in defining the research methods and specific targets for the study.
*   **Graph Creation (Roocode):**
    *   Use "Gemini in Roocode" (this refers to a development environment like VS Code integrated with Gemini capabilities) to write Python scripts for generating graphs from raw data.
    *   Organize the output graph files into appropriate folders.
*   **Textual Summaries (Roocode):**
    *   Within "Roocode," also generate JSON files that contain textual summaries of the research results.

## Step 4: Summarize Result

*   Develop a final summary of the research findings.
*   This summary should be contextualized by and integrate with the combined document created in Step 2.

## Step 5: Create TeX Report

*   **Report Generation:** Create the formal research report as a `.tex` file using LaTeX.
*   **Bibliography:** Manage citations and generate the bibliography using a `references.bib` file.
*   **Debugging (Roocode):** Use "Roocode debug" (debugging features within the IDE, possibly with LaTeX-specific extensions) to troubleshoot and refine the `.tex` document.

## Existing Research Projects

The following projects currently exist in the `research_outputs` directory:

*   `alchohol_retrograde_memory_facilitation`
*   `bockel_thesis`
*   `opiods`