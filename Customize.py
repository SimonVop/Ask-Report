import streamlit as st
from Embedding import *
from Authent import * 


st.set_page_config(page_title="Ask Me Reports", page_icon="💡", layout="wide")   

col1a, col2a, col3a = st.columns([2,3,2])
uploaded_file = st.file_uploader("Please upload File")
try:
    extraction = Extract(uploaded_file)
    data = extraction.extract_text()
    # tables = extraction.extract_table()
    dataframe = create_dataframe()
    index = create_text_embedding()   

    question = st.text_input('Please enter your question here:')
    st.write(':green[Report ready]')
    if question:
        question_embeddings = create_question_embeddings(question)
        answer = get_info(question_embeddings, index)
        st.write(answer)

except:
    st.warning('Upload File first')