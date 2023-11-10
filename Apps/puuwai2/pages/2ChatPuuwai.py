import streamlit as st
import openai
import logging


# .streamlit/secrets.toml
OPENAI_API_KEY = "YOUR_API_KEY"

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
logging.info(f"Messages length {len(st.session_state.messages)}")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def call_gpt(messages):
    logging.info(f"Calling GPT with {len(messages)} messages")
    responses=openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
    return (responses)

def display_response(responses,full_response,message_placeholder):
    for response in responses:
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    logging.info(f"Full Response: \n**** \n {full_response}\n**** \n")
    logging.info(f"Appending response, total back and forth conversations = {len(st.session_state.messages)}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})


context = f"""\nYou are a Cardio Vascular Health advisor and you should provide information only from American Heart Association (heart.org) and ahajournals.org websites\n
Following is my health profile:\n
Body Mass Index: {st.session_state.bmi},\n 
Age: {st.session_state.age},\n 
Gender: {st.session_state.gender},\n
Smoking Status: {st.session_state.nicotine}\n
Healthy Eating Percentile: {st.session_state.mepa}\n
Average hours/day of Sleep: {st.session_state.sleep}\n
Last non-HDL Cholesterol: {st.session_state.lipids}\n
Physical Activity in minutes/week: {st.session_state.pa}\n
Average Fasting Glucose: {st.session_state.glucose}\n
Average Blood Pressure - systolic over diastolic: {st.session_state.sbp} over {st.session_state.dbp}\n

Given this information, answer the following question in less than 2 paragraphs:\n 
"""
# logging.info(f"Initializing Prompt \n {context}")

prompt_for_hints = context+"\n Only Hint me three questions I can ask you? Keep the Questions very short and don't repeat the prompt"

# Accept user input
if prompt := st.chat_input(f"Ask me anything...\n"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
    messages=[{"role": m["role"], "content": context+m["content"]} for m in st.session_state.messages]
    logging.info(f"Calling GPT with {len(messages)} messages")
    display_response(call_gpt(messages),full_response,message_placeholder)

logging.info(f"Session State Messages: {st.session_state.messages}")
if (len(st.session_state.messages)==0):
    messages=[
            {"role": "system", "content": "You are a health assistant."},
            {"role": "user", "content": prompt_for_hints}
        ]
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.markdown("I can answer questions like...\n")
        full_response = ""
    display_response(call_gpt(messages),full_response,message_placeholder)
    logging.info(f"Initializing Question for hints with Messages {messages}")
    
