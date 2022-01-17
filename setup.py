import setuptools
import sys

with open("README.md", "r") as fh:

    long_description = fh.read()

with open ('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(

    name="halfords_search",

    version="1.0.0",

    author="Lewis Chambers",

    author_email="lewis.n.chambers@gmail.com",

    description="Halfords Search Tool",

    url="https://github.com/lewis-chambers/halfords_search_tool",

    install_requires=requirements,
    
    packages=setuptools.find_packages(),

    python_requires='>=3',

)
