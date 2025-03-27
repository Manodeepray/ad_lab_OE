import streamlit as st
import os
from tempfile import NamedTemporaryFile
import skills , projects , llm , utils
import PyPDF2



# Initialize session state variables
if 'resume_path' not in st.session_state:
    st.session_state.resume_path = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'skill_page' not in st.session_state:
    st.session_state.skill_page = {}
if 'project_page' not in st.session_state:
    st.session_state.project_page = {}


def home_page():
    st.title("Resume Analyzer")
    st.write("Upload your resume and paste the job description to get insights")
    
    # File uploader

    # Define directory
    RESUME_DIR = "./uploaded_resumes"
    os.makedirs(RESUME_DIR, exist_ok=True)  # Ensure directory exists

    # File uploader for resume (PDF only)
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        # Generate a safe file path
        resume_text = utils.get_resume_from_bytes(uploaded_pdf=uploaded_file)

        st.session_state.resume_text = resume_text


        # Debugging print (optional)

        st.success("Resume uploaded successfully!")    # Save the file temporarily
        # with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        #     tmp_file.write(uploaded_file.getvalue())
        #     st.session_state.resume_path = tmp_file.name
    
    # Job description input
    st.session_state.job_description = st.text_area(
        "Paste the job description here:",
        height=200,
        value=st.session_state.job_description
    )
    
    if st.button("Analyze Resume"):
        if st.session_state.resume_text and st.session_state.job_description:
            st.success("Analysis started! Navigate to Skills or Projects tabs.")
        else:
            st.warning("Please upload a resume and provide a job description")


def skills_page():
    st.title("Skills Analysis")
    
    if st.button("Run Skills Analysis"):
        Model_object  = llm.GroqModel()
        
        skills_section =  skills.SkillsSection(Model_object= Model_object , resume_text=st.session_state.resume_text, job_description=st.session_state.job_description) # This populates st.session_state.project_page
        st.session_state.skill_page  = skills_section.skill_analysis()
    
    if st.session_state.skill_page:
        # Current Skills Section
        with st.expander("🛠️ Your Current Skills", expanded=False):
            if st.session_state.skill_page["curr_skills"]:
                curr_skills = st.session_state.skill_page["curr_skills"]
                curr_skills_col = st.container()  # Creates a container for content
                curr_skills_col.write(curr_skills)

            else:
                st.warning("No skills found in resume")

        # Job-Required Skills Section
        with st.expander("📋 Job-Required Skills", expanded=False):
            if st.session_state.skill_page["job_skills"]:
                req_skills = st.session_state.skill_page["job_skills"]
                req_skills_col = st.container()
                req_skills_col.write(req_skills)
                
            else:
                st.warning("No job skills data available")

        # Skills Gap Analysis Section
        with st.expander("📈 Skills Gap Analysis", expanded=False):
            if st.session_state.skill_page["comparision"]:
                comparision = st.session_state.skill_page["comparision"]
                
                comparision_col = st.container()
                comparision_col.write(comparision)
            else:
                st.warning("No analysis available")
    else:
        st.info("Run skills analysis to see results")






def projects_page():
    st.title("Projects Analysis")
    
    if st.button("Run Projects Analysis"):
        Model_object = llm.GroqModel()
        projects_section =  projects.ProjectsSection(Model_object= Model_object , resume_text=st.session_state.resume_text, job_description=st.session_state.job_description) # This populates st.session_state.project_page
        st.session_state.project_page  = projects_section.project_analysis()
        
        
    if st.session_state.project_page:
        # Current Projects Section
        with st.expander("📂 Your Current Projects", expanded=False):
            if st.session_state.project_page["curr_projects"]:
                curr_projects = st.session_state.project_page["curr_projects"]
                curr_projects_col = st.container()
                curr_projects_col.write(curr_projects)
            else:
                st.warning("No current projects found in resume")

        # Job-Relevant Projects Section
        with st.expander("🔍 Job-Relevant Projects", expanded=False):
            if st.session_state.project_page["job_projects"]:
                job_projects = st.session_state.project_page["job_projects"]
                job_projects_col = st.container()
                job_projects_col.write(job_projects)
            else:
                st.warning("No job-relevant projects identified")

        # Analysis Section
        with st.expander("📊 Project Analysis Summary", expanded=False):
            if st.session_state.project_page["analysis"]:
                job_analysis = st.session_state.project_page["analysis"]
                job_analysis_col = st.container()
                job_analysis_col.write(job_analysis)
            else:
                st.warning("No analysis available")
    else:
        st.info("Run projects analysis to see results")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Skills", "Projects"])
    
    if page == "Home":
        home_page()
    elif page == "Skills":
        skills_page()
    elif page == "Projects":
        projects_page()
    
    # Clean up temporary file when done
    if hasattr(st.session_state, 'resume_path') and st.session_state.resume_path:
        try:
            os.unlink(st.session_state.resume_path)
        except:
            pass

if __name__ == "__main__":
    main()