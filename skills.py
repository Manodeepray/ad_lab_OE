import llm
import utils




class SkillsSection:
    
    def __init__(self ,Model_object :llm.GroqModel ,resume_text : str  , resume_path : str  = None, job_description : str = None):
        
        # self.resume = utils.get_resume_content(pdf_path=resume_path)
        self.resume = resume_text 
        self.job_description = job_description
        self.Model = Model_object
        self.skill_page = {
            "curr_skills":None,
            "job_skills":None,
            "comparision":None,
        }
        
            
    def get_curr_skills_from_resume(self) -> str:
    
        curr_skills = self.Model.get_response(query = "extract and provide only the current skills from the context",context = self.resume)
        
        self.skill_page['curr_skills'] = curr_skills
        
        
        return curr_skills        
        
    def get_skills_for_job(self) -> str:
        
        job_skills  = self.Model.get_response(query = "get all the skills required for the job description given",context = self.job_description)

        self.skill_page['job_skills'] = job_skills
        
        
        return job_skills     
        
        
    def compare_skillset(self) -> str:
        
        
        context = f"""current skillset of the individual = {self.skill_page['curr_skills']}
        required skillset for the job = {self.skill_page['job_skills']} """
        comparision = self.Model.get_response(query = "comapre and analyse current skills and the skills required for the job description given",context = context)
        
        self.skill_page['comparision'] = comparision
        return comparision  
    
    
    def get_resources(self):
        pass    
    
    def skill_analysis(self):
        _ = self.get_curr_skills_from_resume()
        _ = self.get_skills_for_job()
        _ = self.compare_skillset()
        
        return self.skill_page
        


if __name__ == "__main__":
    
    
    job = input("enter job description : ")
    
    
    Model_object  = llm.GroqModel()
    section = SkillsSection(Model_object , resume_path= "./resume/manodeep_resume_2025_march1.pdf" , job_description=job)
    
    print(section.compare_skillset())