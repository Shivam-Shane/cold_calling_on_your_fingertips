from resumereader import extract_content_from_resume
from jobposting_fetcher import posting_fetcher
from logger import logging
from LLM_process import *

signature=r"""
            Warm regards<br>
            Shivam <br>
            ML Engineer
            <p>Phone: +91-98155-44235
            Email: sk0551460@gmail.com
            <a href="{https://github.com/Shivam-Shane}">GitHub</a> | <a href="{https://www.linkedin.com/in/shivam-2641081a0/}">LinkedIn</a> | <a href="{https://shivam-shane.github.io/My_portfolio_website/index.html}">Portfolio</a>
            </p>
            <p>---------------------------------------------------------------------------------------------------------
            </p><p>▽ Switch off as you go | Recycle - Use Less tissues | Print only if necessary</p>
            ---------------------------------------------------------------------------------------------------------

            <p>This document should only be read by those persons to whom it is addressed and is not intended to be relied upon by any person without subsequent written confirmation of its contents. If you have received this email message in error, please destroy it and delete it from your computer. Any form of reproduction, dissemination, copying, disclosure, modification, distribution, and/or publication of this email message is strictly prohibited.
            </p> """     

Aicontent="""<p>This email was generated using AI models and may include sensitive or potentially misleading information</p>"""

def preview_mail(recipient_name, company_name,url,resume_path):
    if recipient_name == "":
        recipient_name = "Hiring Manager"

    if url:
        resume_data=extract_content_from_resume(resume_path)
        logging.info("extraction done")
        docu=posting_fetcher(url)
        logging.info("url extraction done")

        result=create_email_template(docu,resume_data)
        print(result.content)
        logging.info(result.content+signature)
        return result.content+signature+Aicontent
    else: # otherwise hard-code template will be created
        body = f"""Dear {recipient_name},
                <p>I hope this email finds you well. My name is Shivam.
                and I am an aspiring Machine Learning Engineer with nearly three years of experience in IT, focusing on developing and deploying scalable machine learning models and workflows. 
                        
                        <p>I came across your organization {company_name}.
                        I would love to explore any opportunities where I could contribute my skills in AI and automation.
                        
                        Throughout my career, I have built expertise in Python, TensorFlow, and Scikit-learn, as well as DevOps tools such as Docker and Kubernetes. 
                        <p>In my most recent role at Indus Valley Partners, I led the development of a custom monitoring system that automated the categorization of critical service alerts, reducing response times by 77%. 
                        I have also worked on machine learning projects, including an AI-powered image caption generator and an automated text summarization tool, 
                        demonstrating a track record of delivering impactful solutions.</p>
                        
                        I would be thrilled to discuss how my skills in machine learning, DevOps, and cloud technologies could be valuable to your team. 
                        </p><p>I am attaching my resume for your reference and would appreciate the opportunity to connect further.
                        
                        </p>Thank you for your time and consideration. I look forward to your response.

                        <p>Warm regards,</p>
                        Shivam
                        <p>ML Engineer</p>
                        Phone: +91-98155-44235
                        Email: sk0551460@gmail.com
                        <p>GitHub | LinkedIn | Portfolio</p>

                        ---------------------------------------------------------------------------------------------------------
                        <p>▽ Switch off as you go | Recycle - Use Less tissues | Print only if necessary
                        </p>---------------------------------------------------------------------------------------------------------

                        </p>This document should only be read by those persons to whom it is addressed and is not intended to be relied upon by any person without subsequent written confirmation of its contents. If you have received this email message in error, please destroy it and delete it from your computer. Any form of reproduction, dissemination, copying, disclosure, modification, distribution, and/or publication of this email message is strictly prohibited.
                """
    return body
