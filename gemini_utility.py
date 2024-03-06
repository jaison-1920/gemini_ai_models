import os
import json

import google.generativeai as genai


# while running streamlit, it doesn't recognize this directory
# as the default directory. for that we are navigating to this
# directory
working_directory = os.path.dirname(os.path.abspath(__file__))


#loading the json file
config_flie_path = f"{working_directory}/config.json" #navigating the path of file
config_data = json.load(open(config_flie_path))  #storing into a variable

google_api_key = config_data["GOOGLE_API_KEY"]  # storing the api_key


#configuring google.generativeai with api_key
genai.configure(api_key=google_api_key)

#function for load gemini-pro model for chatbot
def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

#function for image captioning
def gemini_pro_vision_response(promt,image):
    gemini_vision_model = genai.GenerativeModel("gemini-pro-vision")
    response = gemini_vision_model.generate_content([promt,image])
    result = response.text
    return result

#function for embedding
def embedding_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list

