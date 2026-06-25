import streamlit as st
from google import genai 
import os
Gemini_API_Key=os.getenv("Gemini_API_Key") 
client = genai.Client(api_key=Gemini_API_Key ) 
def save_chat(user,ChatBot):
    with open ("chat_history.txt","a",encoding="utf-8") as file:
        file.write(f"you:{user}\n") 
        file.write(f"ChatBot: {ChatBot}\n\n") 

def read_chat():
    try:
        with open("chat_history.txt","r",encoding="utf-8")as file:
            return file.read()
    except:
        return ""
    
st.title("Python Tutor AI")
st.caption("Learn python with an AI tutor")
if "chat" not in st.session_state:
    st.session_state.chat = []
with st.sidebar:
    st.header("ChatBot Menu")
    st.write("Total Messages:", len(st.session_state.chat))
    st.write("Questions Asked:", len(st.session_state.chat)//2)

    if st.button("Clear Chat"):
        st.session_state.chat=[]
        st.rerun()

    chat_data = read_chat()

    st.download_button(
        label="Download Chat",
        data=chat_data,
        file_name="chat_history.txt",
        mime="text/plain"
    )

    st.subheader("Saved History")
    
    if chat_data.strip():
        st.text_area(
            "History",
            chat_data,
            height=200,
            disabled= True
        )
 
system_prompt = """You are a Python Tutor AI.

Your job is to:
- Teach Python to beginners
- Explain code line by line
- Help with debugging
- Give hints before solutions
- Encourage problem solving"""

user = st.chat_input("Type your message")
    
if user:
    st.session_state.chat.append({"role": "user", "content": user})
    conversation = system_prompt + "\n"
    for message in st.session_state.chat:
        if message["role"] == "user":
            conversation += f"User: {message['content']}\n"
        else:
            conversation += f"Assistant: {message['content']}\n"

    try:
        with st.spinner("Thinking..."):
            response = client.models.generate_content(   
                model = "gemini-2.5-flash", 
                contents = conversation
            )
        ChatBot_reply = response.text

    except Exception as e:
        ChatBot_reply = f"Error: {str(e)}"

    st.session_state.chat.append({"role": "assistant", "content": ChatBot_reply})
    save_chat(user,ChatBot_reply)

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])