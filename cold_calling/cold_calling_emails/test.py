import os
import sys
# Adding the project root directory to the PYTHONPATH for imports from upper level
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_path)

from customize_email_content import custom_email_content

get_email_details_object=custom_email_content()

result=get_email_details_object.get_email_content()
if not result:
    result=['None']
    print("No email content found.",result)

else:
    print(result[0]['your_name'])
