from customize_email_content import custom_email_content
get_email_details_object=custom_email_content()
from utility import read_yaml

def mail_content_handler(recipient_name, company_name, company_work_related):
        """Handles mail body to process like html content"""
        result=get_email_details_object.get_email_content()
        config=read_yaml('config.yaml')
        if recipient_name=="":
                recipient_name="Hiring Manager" # default recipient
        # Define the social media links
        Sender_name=result[0]['your_name']
        Sender_phone=result[0]['phone_no']
        Sender_email=config['SMTP_USERNAME']
        
        links = {
        'GitHub': result[0]['github_link'],
        'LinkedIn': result[0]['linkedin_link'],
        'Portfolio': result[0]['portfolio_link']
                }
        signature_parts = [f'<a href="{url}">{name}</a>' for name, url in links.items() if url]

        finalsignature=str()
        for signature_part in signature_parts:
                finalsignature += signature_part + " | "

        body=f"""
                <html>
                    <body>
                        <p>Dear {recipient_name},</p>
                        <p>I hope this email finds you well. My name is Shivam, 
                        and I am an aspiring Machine Learning Engineer with nearly three years of experience in IT, 
                        focusing on developing and deploying scalable machine learning models and workflows. 
                        I came across your organization {company_name} and was impressed by your innovative work in the field 
                        of {company_work_related}. I would love to explore any opportunities where I could contribute my skills in AI and automation.</p>
                        
                        <p>Throughout my career, I have built expertise in Python, TensorFlow, and Scikit-learn, as well as DevOps tools such as Docker and Kubernetes. In my most recent role at Indus Valley Partners, I led the development of a custom monitoring system that automated the categorization of critical service alerts, reducing response times by 77%. I have also worked on machine learning projects, including an AI-powered image caption generator and an automated text summarization tool, demonstrating a track record of delivering impactful solutions.</p>
                        
                        <p>I would be thrilled to discuss how my skills in machine learning, DevOps, and cloud technologies could be valuable to your team. I am attaching my resume for your reference and would appreciate the opportunity to connect further.</p>
                        
                        <p>Thank you for your time and consideration. I look forward to your response.</p>

                        <p>Warm regards,<br/>
                        {Sender_name}<br/>
                        
                        Phone: {Sender_phone}<br/>
                        Email: <a href="mailto:{Sender_email}">{Sender_email}</a><br/>
                        {finalsignature}
                        


                        <p>----------------------------------------------------------------------------------------------<br/>
                        ▽ Switch off as you go | Recycle - Use Less tissues | Print only if necessary<br/>
                        ---------------------------------------------------------------------------------------------------------</p>

                        <p>This document should only be read by those persons to whom it is addressed and is not intended to be relied upon by any person without subsequent written confirmation of its contents. If you have received this email message in error, please destroy it and delete it from your computer. Any form of reproduction, dissemination, copying, disclosure, modification, distribution, and/or publication of this email message is strictly prohibited.</p>
                    </body>
                </html>
                """
        return body