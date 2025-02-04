from langchain.prompts import PromptTemplate

# Define the prompt template for extracting job post details from career page
prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
)

email_template_prompt=PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM JOB WEBSITE AND CANDIDATE RESUME TO CREATE AN EMAIL TEMPLATE FOR COLD CALLING:
        Job Posting: {job_posting}
        Candidate Resume: {candidate_resume}
        
        ### INSTRUCTION:
        - The scraped text is from the career page of a website.
        - Your job is to analyze the job postings and the candidate resume.
        - Return a professional, well-formed cold calling email body tailored to the job posting and candidate's qualifications.

        ### OUTPUT:
        - A valid email template in HTML/CSS formate with no preamble or extraneous text and no email signature.
        """
    )