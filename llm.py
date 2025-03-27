
import os
from groq import Groq

from dotenv import load_dotenv

load_dotenv(dotenv_path = '.env')


class GroqModel:
    def __init__(self, model : str ='gemma2-9b-it' ):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        self.model = model  # Example: 'mixtral-8x7b'




    def get_response(self, query : str, context :str) -> str:
        prompt = f"""
        Answer the following question based on the context given below:
        
        Query: {query}
        Structure: {context}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        print(response.choices[0].message.content.strip())
        
        return str(response.choices[0].message.content.strip())

    


if __name__ == "__main__":
    
    model = GroqModel()
    question = "show all the user with marks less than 80"
        
    response = model.get_response(query = "what colour is sky" , context = "sky is blue")
