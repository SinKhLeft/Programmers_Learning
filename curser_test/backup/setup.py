from setuptools import setup, find_packages

setup(
    name="board_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Django==5.0.2",
        "python-dotenv==1.0.0",
    ],
) 