import os
import openai
import streamlit as st
from streamlit_chat import message
import json
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_text():
    s = st.empty()
    uin = s.text_input("You: ")
    if uin == "":
        return ""
    st.session_state.past.append(uin)
    message(uin, is_user=True)
    s.empty()
    return uin

def generate_text(prompt):
    completions = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt='Give the title, synopsis, currently active image URL, trailer URL, genre in JSON array of this format with these keys {"title","synopsis","image","trailer","genre"} of a few movie best matching the following description and make sure to sanitize it properly to valid json and always give a json array: ' + prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return completions.choices[0].text

def handle_recommendation(response):
    print(response)
    responses = json.loads(response[response.find('['):])
    for response in responses:
        st.image(response['image'])
        out = f"Title: {response['title']}\n\nSynopsis:\n{response['synopsis']}\n\nGenre(s): {response['genre']}\n\nWatch the trailer [here]({response['trailer']})!"
        print(out)
        st.session_state.generated.append(out)
        st.write(out)

def get_recommendation():
    if len(st.session_state.past) == 0:
        return
    prompt = st.session_state.past[-1]
    handle_recommendation(generate_text(prompt))

def add_buttons():
    pass

def init():
    print("INIT")
    st.title("Mort")
    message("Hey there! What would you like to watch today?")
    if 'turn' not in st.session_state:
        st.session_state['turn'] = 'user'
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
        # st.session_state.generated.append("Hey there! What would you like to watch today?")
    if 'past' not in st.session_state:
        st.session_state['past'] = []
        get_text()
        return

    for i in range(len(st.session_state.generated)):
        message(st.session_state.past[i], is_user=True)
        message(st.session_state.generated[i])
    if get_text() != "":
        get_recommendation()
    add_buttons()

init()
