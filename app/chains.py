import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# Initialize the chain
class Chain:
    def __init__(self):
        # Initialize the language model (creates an instance of ChatGroq language model)
        self.llm= ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"),
                                   model_name='llama-3.1-8b-instant')
        
    def extract_jobs(self, text):
        # Define the prompt template for extracting job information
        prompt_extract = PromptTemplate.from_template(
        '''
        "Extract the relevant information from the following text: {input_text}
        ### Instruction:
        The scraped text is from the career's page of a website.
        your task is to extract the relevant information from the text in json format containing following keys:
        'role', 'experience', 'skills', 'description'.
        only return the valid JSON.
        ### VALID JSON (NO PREAMBLE)
        '''
        )
        # Create the extraction chain
        chain_extract = prompt_extract | self.llm
        # Invoke the chain with the input text
        res = chain_extract.invoke(input={'input_text': text})
        try:
            # Parse the JSON output
            json_parser = JsonOutputParser()
            job = json_parser.parse(res.content)
        except OutputParserException as e:
            raise ValueError(f"Failed to parse LLM output: {e}")
        # Ensure the output is a list
        return job if isinstance(job, list) else [job]

    # Define the prompt template for writing the email
    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Faren, a business development executive at PPP. PPP is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of PPP
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase PPP's portfolio: {link_list}
            Remember you are Mohan, BDE at PPP. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            
            """
        )
        # Create the email generation chain
        email_prompt = prompt_email | self.llm
        # Invoke the chain with the input data
        res = email_prompt.invoke(input={'job_description': str(job), 'link_list': links})
        return res.content
