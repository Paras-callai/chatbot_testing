import requests
import json
import os
import streamlit as st


def bot_response(url, data ):

    payload = json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def file_selector(folder_path):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()