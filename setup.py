from setuptools import setup, find_packages

setup(
    name="insurance-chatbot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pdfplumber',
        'langchain',
        'python-dotenv',
        'faiss-cpu',
    ]
)