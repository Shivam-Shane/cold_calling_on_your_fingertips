# Cold Email Automation

## Overview
Cold Email Automation is a tool that streamlines the process of sending personalized cold emails to potential recruiters. The project aims to enhance the efficiency of outreach efforts by automating the generation and dispatch of emails, reducing manual work, and ensuring higher engagement rates through customization.

## Features
- **Automated Email Sending**: Send emails automatically to the recuriters.
- **Job Post Extraction and Crafting Email** Extract content from the job post url and generate email based on job post and matching details provided in resume. 
- **Personalization**: Use placeholders for custom fields (e.g., recipient's name, company) to personalize each email.

## Error Handling:

The system includes error handling mechanisms to manage cases where the email content doesn't match any rule or if any other issue arises, while sending mails.

## Requirements
- **Python 3.11+**
- **Gmail App Password**
- **Additional Libraries**: Listed in `requirements.txt`
- **SQL SERVER and DATABASE to store email, and configuration data**

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Shivam-Shane/cold_calling_on_your_fingertips.git
    cd cold_calling
    Creator database schema by running the `creator_database_schema.sql` script in your SQL Server.
    ```

2. **Install dependencies**
    ```bash
    Install the Required Libraries:
    pip install -r requirements.txt

    Follow the instructions here to enable the Gmail APP password
    https://support.google.com/mail/answer/185833?hl=en
    ```
## Demo:

![Demo Gif](demo/cold_calling.gif)

## Logs:

All actions and errors are logged for troubleshooting and auditing purposes. Check the logs/ directory for log files.

## Contribution
Feel free to fork this project, submit pull requests, or report issues. Contributions to enhance the functionality and make the system more robust are welcome!

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.

## Contact

For questions, suggestions, or support, reach out at 
- **sk0551460@gmail.com** 
- **shivam.hireme@gmail.com**.

## Support the Project

Help support continued development and improvements:

- **Follow on LinkedIn**: Stay connected for updates – [LinkedIn Profile](https://www.linkedin.com/in/shivam-hireme/)
- **Buy Me a Coffee**: Appreciate the project? [Buy Me a Coffee](https://buymeacoffee.com/shivamshane)
- **Visit Portfolio**: [Shivam's Portfolio](https://shivam-portfoliio.vercel.app/)
