from dotenv import load_dotenv
load_dotenv()
import os

import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to load Gemini Pro model and get repsonse

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

#Initialize our streamlit app
st.set_page_config(page_title="Conversational Q&A")
st.header("Gemini LLM Application")

#Initialize session state for chat History if it doesnt exist
if 'chat_history' not in st.session_state:    # if there is not chat history
    st.session_state['chat_history']=[]       # Create a chat history
    
input=st.text_input("Input:",key="input")
submit=st.button("Ask a question")

if submit and input:
    response=get_gemini_response(input)
    #Add user query and response to session chat history
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))
st.subheader("The Chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
        
    
