import streamlit as st
import pandas as pd
import openai

# Load your dataset
df = pd.read_csv(r'data\F_DIS_DS_WHS_half.csv')

# **Don't store the API key directly in the code!**

# Load HTML content from external file
with open('template.html', 'r') as f:
    html_content = f.read()

# Display HTML content in Streamlit
st.markdown(html_content, unsafe_allow_html=True)

#st.title("HEINEKEN RECOMMENDATION")

# Display table with header styling
st.subheader("Dataset Preview")
with st.expander("Show Dataset"):
    st.write(df.head(10).to_html(), unsafe_allow_html=True)

st.subheader("Ask a Question:")
user_question = st.text_input("Enter your question:")

if st.button("Submit"):  # Changed "summit" to "Submit" for better grammar
    try:
        # Load the API key from environment variables
        api_key = os.environ["OPENAI_API_KEY"]

        # Initialize the OpenAI client with your API key
        openai.api_key = api_key

        # Preprocess the dataset (example: convert to a list of dictionaries)
        dataset_summary = df.to_dict(orient='records')

        # Create the prompt with dataset context
        prompt = f"""Here's some data: {dataset_summary}

        Please answer the following question based on the provided data: 
        {user_question}
        """

        # Make a call to the OpenAI API for chat completions
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract and display only the answer from the AI response
        ai_response = completion.choices[0].message['content']
        st.write("AI Answer:")
        st.write(ai_response)
    except KeyError:
        st.error("Please set the environment variable 'OPENAI_API_KEY' with your API key")
