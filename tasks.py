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

from agents import researcher, profiler, resume_strategist, interview_preparer


## Create the tasks

# Task for Researcher Agent: Extract Job Requirements
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher,
    async_execution=True
)

# Task for Profiler Agent: Compile Comprehensive Profile
profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub ({github_url}) URLs, and personal write-up "
        "({personal_writeup}). Utilize tools to extract and "
        "synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=profiler,
    async_execution=True
)

# Task for Resume Strategist Agent: Align Resume with Job Requirements
resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "inlcuding the initial summary, work experience, skills, "
        "and education. All to better reflrect the candidates "
        "abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist
)

# Task for Interview Preparer Agent: Develop Interview Materials
interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these question and talking points to "
        "help the candiadte highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)


## Creating the CREW
job_application_crew = Crew(
    agents=[researcher,
            profiler,
            resume_strategist,
            interview_preparer],

    tasks=[research_task,
           profile_task,
           resume_strategy_task,
           interview_preparation_task],

    verbose=True
)

## Running the Crew
# Set the inputs for the execution of the crew.

job_application_inputs = {
    'job_posting_url': 'https://www.google.com/search?q=IBM+Generative+AI+developer+job&oq=IBM+Generative+AI+developer+job&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQLhhA0gEJMTM0NzFqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&htidocid=QW-A1gKy_AIkmQGNAAAAAA%3D%3D&sa=X&ved=2ahUKEwik3qaz57WGAxXmk1YBHbjXAHkQkd0GegQIERAB#fpstate=tldetail&htivrt=jobs&htiq=IBM+Generative+AI+developer+job&htidocid=QW-A1gKy_AIkmQGNAAAAAA%3D%3D&sxsrf=ADLYWIIMiqTXv_35TSLVUbF9aCG8-yLomg:1717086961911',
    'github_url': 'https://github.com/Ram580',
    'personal_writeup': """Highly motivated and results-oriented Data Analyst with 2.5 years of experience driving data-driven decision making through advanced analytics, ML, Deep learning, NLP and Generative AI solutions.
    adept at various domains – marketing analytics , manufacturing, pharma and airlines.  and expert in multiple
    programming languages and frameworks.His Experties are Advanced Analytics : Utilized Machine learning(Regression, Classification, Time series forecasting), Deep Learning (LSTM), NLP, and GenAI (Langchain) to solve complex business problems in Pharma and Healthcare.
ETL Pipeline Development: Built and automated efficient ETL pipelines  leveraging Python, SQL, PySpark that reduced data turnaround time by 30%.
Generative AI: Expertise in LLM fine-tuning (PEFT), RLHF, prompt engineering for various AI models, RAG Applications, Multimodal AI applications development, evaluation and deployment,
Actionable Insights & Dashboards: Created high-performance dashboards (Power BI, Tableau) to empower data-driven decision making (e.g., patient churn reduction).
Forecasting & Modeling: Built, finetuned and enhanced multiple forecasting models for various use cases like regression, classification, time series forecasting etc.,
Project Leadership: Mentored data science interns and led junior analysts in various data science projects (EDA to deployment).
Cross-Industry Experience: Possesses experience in diverse sectors (Pharma, Healthcare, Airlines).
Project Versatility: Implemented projects ranging from prescriber choice model for measuring campaign effectiveness in pharma, airline resource allocation (passenger footfall forecasting), Gen AI knowledge repositories chatbot (Langchain, LLMs).
Cloud and Deployment Skills: Utilized tools like Docker, Git, Github Actions and AWS Sagemaker, Amazon Bedrock, S3, AWS Lambda, API Gateway, AWS RDS for project deployments
"""
}

### this execution will take a few minutes to run
def kickoff_crew(inputs):
    result = job_application_crew.kickoff(inputs=inputs)
    return result
    

# from IPython.display import Markdown, display
# display(Markdown("./tailored_resume.md"))