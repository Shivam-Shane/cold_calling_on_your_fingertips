from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from prompts import *
import os
from dotenv import load_dotenv
json_resultparser=JsonOutputParser()
load_dotenv()

llm = ChatGroq(
    temperature=0, 
    groq_api_key=os.getenv('GROC_LLM_API'), 
    model_name=os.getenv('LLM_MODEL_NAME')
)

# Define the chain to extract job post details using LLM
chain_extract_pipe = prompt_extract | llm 
email_template_pipe = email_template_prompt | llm

def extract_job_post_details(documents):
    """
    Extracts job post details from a list of documents extracted from the url.
    """
    result=chain_extract_pipe.invoke(input={'page_data':documents})
    result=json_resultparser.parse(result.content)
    return result

# Function to generate the email template
def create_email_template(job_posting, candidate_resume):
    try:
        # Ensure inputs are non-empty
        if not job_posting:
            raise ValueError("Job posting text cannot be empty.")
        if not candidate_resume:
            raise ValueError("Candidate resume text cannot be empty.")
        
        # Generate email template
        result = email_template_pipe.invoke(input={'job_posting': job_posting, 'candidate_resume': candidate_resume})
        return result
    except Exception as e:
        return f"An error occurred while generating the email template: {e}"