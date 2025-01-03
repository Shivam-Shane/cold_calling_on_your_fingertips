
from setuptools import setup, find_packages

def get_requirements(file_path: str):
    requirements = []
    with open(file_path,encoding="utf-8") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements

setup(
    name="coldcalling",
    version="1.0.1",
    packages=find_packages(),
    py_modules=["logger",'util'], 
    author="SHIVAM",
    author_email="sk0551460@gmail.com",
    description="For sending cold calls to recruiter and referral",
    # long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::  GPL-3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.3',
    install_requires=get_requirements('requirements.txt'),
)
