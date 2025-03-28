import streamlit as st
import requests

API_URL = "http://localhost:8000/process_request"

st.set_page_config(page_title="AI Orchestrator", layout="centered")
st.markdown("<h1 style='text-align: center;'> AI Task Orchestrator</h1>", unsafe_allow_html=True)

st.markdown("###  What do you want to do?")
user_request = st.text_input("", placeholder="e.g., Clean the text and analyze sentiment or summarize it.")

st.markdown("###  Enter your text below:")
text_data = st.text_area("", height=200)

if st.button(" Run Orchestrator", type="primary"):
    if not user_request or not text_data:
        st.warning(" Please provide both a task instruction and some input text.")
    else:
        with st.spinner(" Talking to the LLM and running container tasks..."):
            try:
                response = requests.post(API_URL, json={
                    "user_request": user_request,
                    "text": text_data
                })

                if response.status_code == 200:
                    result = response.json()

                    if "error" in result:
                        st.error(f" Orchestrator Error: {result['error']}")
                    else:
                        st.success(" All tasks completed successfully!")

                        st.markdown("###  Final Output")
                        st.code(result["final_result"], language="text")

                        with st.expander(" View All Task Outputs"):
                            st.markdown("####  Task Plan")
                            st.write(" → ".join(result.get("plan", [])))

                            st.markdown("####  Intermediate Outputs")
                            for task, output in result.get("outputs", {}).items():
                                st.markdown(f"**🔹 {task.replace('_', ' ').title()}:**")
                                st.code(output)

                else:
                    st.error(f" API Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f" Request failed: {e}")
