from openai import OpenAI
import streamlit as st

st.title("What!🤖TUDU")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Predefined prompt
predefined_prompt = """
Create the timetable for user: I want that when I tell you my today tasks, then according to 24 hr you should create a timetable for me. I would not provide duration, you set it accordingly. The tasks are: {user_tasks}. Do it now for me, create a timetable.
"""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Check if the user wants to create a timetable
    if prompt.lower() == "create the timetable for user":
        # Ask for user tasks
        user_tasks = st.text_input("Please enter your tasks for today:")
        
        # Formulate the prompt with user tasks
        prompt_with_tasks = predefined_prompt.format(user_tasks=user_tasks)
        
        st.session_state.messages.append({"role": "user", "content": prompt_with_tasks})
        
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
