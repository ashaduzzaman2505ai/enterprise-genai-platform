import streamlit as st
import requests

st.set_page_config(page_title="Enterprise GenAI Demo", layout="wide")
st.title("Enterprise GenAI Platform Demo")

st.write("Ask any question about internal policies or governance:")

question = st.text_input("Your Question:")

if st.button("Submit"):
    if question.strip():
        response = requests.post(
            "http://nginx/api/query",
            json={"question": question}
        )
        if response.status_code == 200:
            st.success(response.json()["answer"])
        else:
            st.error(f"Error: {response.status_code}")