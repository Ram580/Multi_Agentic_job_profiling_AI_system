from crewai import Agent, Task, Crew

from dotenv import load_dotenv
import os
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


# Setup the Gemini pro LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, verbose=True, google_api_key=os.environ["GOOGLE_API_KEY"],convert_system_message_to_human=True)

#setup the serper api key
os.environ["SERPER_API_KEY"] = os.getenv("serper")

# Warning control
import warnings
warnings.filterwarnings('ignore')


## First Setup the required Tools for the agents
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  PDFSearchTool,
  SerperDevTool
)

import streamlit as st
# Create the "inputs" folder if it doesn't exist
if not os.path.exists("inputs"):
    os.makedirs("inputs")
# File Upload
#uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

def save_uploaded_file(uploaded_file):
    """
    Saves the uploaded file to the 'inputs' folder.
    """
    file_path = os.path.join("inputs", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Uplading the files to inputs folder
uploaded_file = st.file_uploader("Upload a file")

if uploaded_file:
    saved_file_path = save_uploaded_file(uploaded_file)
    st.success(f"File saved to: {saved_file_path}")

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='inputs\Ram_Resume_2024.pdf')
semantic_search_resume = PDFSearchTool(mdx='inputs\Ram_Resume_2024.pdf')


## Creating the agents

# Agent 1: Researcher
researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job posting to help job applicants",
    tools = [scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in "
        "navigating and extracting critical "
        "information from job postings is unmatched."
        "Your skills help pinpoint the necessary "
        "qualifications and skills sought "
        "by employers, forming the foundation for "
        "effective application tailoring."
    ),
    llm = llm
)

# Agent 2: Profiler
profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Do increditble research on job applicants "
         "to help them stand out in the job market",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Equipped with analytical prowess, you dissect "
        "and synthesize information "
        "from diverse sources to craft comprehensive "
        "personal and professional profiles, laying the "
        "groundwork for personalized resume enhancements."
    ),
    llm = llm
)

# Agent 3: Resume Strategist
resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a "
         "resume stand out in the job market.",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you "
        "excel at refining resumes to highlight the most "
        "relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    ),
    llm = llm
)

# Agent 4: Interview Preparer
interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points "
         "based on the resume and job requirements",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of "
        "interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, "
        "ensuring they can confidently address all aspects of the "
        "job they are applying for."
    ),
    llm = llm
)

