import streamlit as st
from openai import OpenAI
st.title("Provided by of Bashir Aziz")

note= ("""All three pages will provided similar response 
         1. Compute Percent Complete page does not make a call to OpenAI API
         2. Ask me to Compute Percent Complete, makes a call to OpenAI API and uses a custum function to compute the percent complete
         3. Ask me a Question page makes a call to OpenAI API to answer a question and provides a response received from OpenAI API""")

st.markdown(note)