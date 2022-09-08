from setuptools import setup,find_packages
from typing import List


# Declaring variables for setup functions 
PROJECT_NAME = "Housing Price Predictor"
VERSION = "0.0.6"
AUTHOR = "Amit Vikram Raj"
DESCRIPTION = "This is my first complete End-to-End ML project."
PACKAGES = ["housing"]
REQUIREMENTS_FILE_NAME  = "requirements.txt"


def get_requirements_list()->List[str]:
    """
    Description: This function returs the list of requirements
    mention in requirements.txt file

    return returs a list with the name of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENTS_FILE_NAME) as requirements_file:
        return requirements_file.readlines()

setup(
    name = PROJECT_NAME,
    version = VERSION,
    author= AUTHOR,
    description= DESCRIPTION,
    packages= find_packages(),
    install_requires = get_requirements_list().remove("-e .")
)

# Since we are using find_packages() to install our internal pacakges, 
# that's why we are removing "-e ." from install_requires list as it also does the same thing.