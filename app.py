import streamlit as st
from crewai import Crew
from tasks import kickoff_crew

# Create a Streamlit app
st.title("Job Application Profiler & Resume Personalizer")

# import os

# # Create the "inputs" folder if it doesn't exist
# if not os.path.exists("inputs"):
#     os.makedirs("inputs")
# # File Upload
# #uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

# def save_uploaded_file(uploaded_file):
#     """
#     Saves the uploaded file to the 'inputs' folder.
#     """
#     file_path = os.path.join("inputs", uploaded_file.name)
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     return file_path

# # Uplading the files to inputs folder
# uploaded_file = st.file_uploader("Upload a file")
# if uploaded_file:
#     saved_file_path = save_uploaded_file(uploaded_file)
#     st.success(f"File saved to: {saved_file_path}")
    
# Input Variables
job_posting_url = st.text_input("Job Posting URL")
github_url = st.text_input("GitHub URL")
personal_writeup = st.text_area("Personal Write-up")


# Run CrewAI
if st.button("Run CrewAI"):
    # Set inputs for the execution of the Crew
    inputs = {
        "job_posting_url": job_posting_url,
        "github_url": github_url,
        "personal_writeup": personal_writeup,
    }
    result = kickoff_crew(inputs)

    # Initialize the Crew
    job_application_crew = Crew(...)  # Add your Crew initialization here

    # Execute the Crew
    #result = job_application_crew.kickoff(inputs=inputs)

if st.button("Display Tailored Resume"):
    # Display output
    st.markdown(f"## Tailored Resume")
    st.markdown(result["tailored_resume.md"])

if st.button("Display Interview preparation materials"):
    st.markdown(f"## Interview Materials")
    st.markdown(result["interview_materials.md"])