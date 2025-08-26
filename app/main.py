import streamlit as st
from utils import clean_text
from portfolio import Portfolio
from chains import Chain
from langchain_community.document_loaders import WebBaseLoader

# Function to create the Streamlit app
def create_streamlit_app(llm, portfolio, clean_text):
    st.title("GenAI Cold Email Generator")
    url_input = st.text_input("Enter the job URL:", value="https://mycareer.verizon.com/jobs/r-1071918/full-stack-developer")
    submit_button = st.button("Generate Email")

    if submit_button:
        # Call the email generation function here
        # st.code("Email generated successfully!",language="markdown")

        try:
            # Load the job data from the URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            # Process the data to extract job info and generate email
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language="markdown")
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":  
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="GenAI Cold Email Generator", page_icon=":robot_face:")
    create_streamlit_app(chain, portfolio, clean_text)
