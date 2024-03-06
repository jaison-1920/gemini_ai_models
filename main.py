import os

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu

from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_vision_response,
                            embedding_model_response)

# while running streamlit, it doesn't recognize this directory
# as the default directory. for that we are navigating to this
# directory
working_directory = os.path.dirname(os.path.abspath(__file__))


#setting up the page configuration
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)

with st.sidebar:
    selected = option_menu(
        "Gemini_AI",
        ['Chatbot','Image Caption','Text Embedding'],
        default_index=0
    )

# function to translate role between gemini and streamlit
def translate_role_for_streamlit(user_role):
    if user_role=="model":
        return "assistant"
    else:
        return user_role

#for chatbot
if selected=="Chatbot":
    model = load_gemini_pro_model()

    #initialize chat session in streamlit
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    #streamlit page title
    st.title("ChatBot 🤖")

    # display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # input field for user
    user_prompt = st.chat_input("Ask Gemini Pro")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt)


        #display gemini response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# for image caption generator
if selected == "Image Caption":


    #streamlit page title
    st.title("📷Snap Narrate")

    uploaded_image = st.file_uploader("Upload an Image...",type=['jpg','jpeg','png'])

    if st.button("Generate Caption"):
        image = Image.open(uploaded_image)

        col1,col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800,500))
            st.image(resized_image)

        default_prompt= "Write a short caption for this image"

        #getting the response from gemini vision model
        caption = gemini_pro_vision_response(default_prompt,image)

        with col2:
            st.info(caption)

# for text embedding
if selected == "Text Embedding":

    # title of streamlit page
    st.title("🗟 Embed Text")

    #text input box
    input_text = st.text_area(label="",placeholder="Enter the text to get embeddings")

    if st.button("Get embeddings"):
        response = embedding_model_response(input_text)
        st.markdown(response)
