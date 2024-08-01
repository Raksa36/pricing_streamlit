import os
import openai
import streamlit as st
from pandas import DataFrame
from openai import OpenAI
from data import load_data

class StreamlitCallback:
    def __init__(self, container):
        self.container = container

    def on_code(self, response):
        self.container.code(response)

class StreamlitResponse:
    def __init__(self, context):
        self.context = context

    def format_dataframe(self, result):
        st.dataframe(result["value"])

    def format_plot(self, result):
        st.image(result["value"])

    def format_other(self, result):
        st.write(result["value"])

st.write("# HEINEKEN RECOMMENDATION")

df = load_data("./data")

with st.expander("🔎 Dataframe Preview"):
    st.write(df.head(10))

query = st.text_area("🗣️ Chat with Dataframe")
container = st.container()

if query:
    api_key = "sk"
    client = openai(api_key=api_key)

    # Make a call to the OpenAI API for chat completions
    completion = client.chat_completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Process the completion response
    st.write(completion)