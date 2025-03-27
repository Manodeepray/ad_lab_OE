import llm
import utils




class ProjectsSection:
    
    def __init__(self ,Model_object :llm.GroqModel ,resume_text : str  , resume_path : str  = None, job_description : str = None):
        
        # self.resume = utils.get_resume_content(pdf_path=resume_path)
        self.resume = resume_text 
        self.job_description = job_description
        self.Model = Model_object
        
        self.project_page = {
            "curr_projects" : None,
            "job_projects" : None,
            "analysis" : None   
        }
        
            
    def get_curr_projects_from_resume(self) -> str:
    
        curr_projects = self.Model.get_response(query = "extract and provide all details about the projects from the context",context = self.resume)
        
        self.project_page['curr_projects'] = curr_projects
        
        
        return curr_projects        
        
    def get_projects_for_job(self) -> str:
        
        job_projects  = self.Model.get_response(query = "generate some projects that would be required in the resume for the job description given",context = f"job description :{self.job_description}")

        self.project_page['job_projects'] = job_projects
        
        
        return job_projects     
        
        
    def analyze_projects(self) -> str:
        
    
        
        context = f"""current  of the individual = {self.project_page['curr_projects']}
        required projects for the job = {self.project_page['job_projects']} """
        
        analysis = self.Model.get_response(query = "analyse  projects from thge resume and provide strengths , weaknesses and improvement for each project",context = context)
        
        self.project_page['analysis'] = analysis
        return analysis  
    
    
    def get_source(self):
        pass    


    def project_analysis(self):
        _ = self.get_curr_projects_from_resume()
        _ = self.get_projects_for_job()
        _ = self.analyze_projects()
        
        return self.project_page
    
    
if __name__ == "__main__":
    
    
    job = input("enter job description : ")
    
    
    Model_object  = llm.GroqModel()
    section = ProjectsSection(Model_object , resume_path= "./resume/manodeep_resume_2025_march1.pdf" , job_description=job)
    
    print(section.analyze_projects())