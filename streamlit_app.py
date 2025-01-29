import streamlit as st
import google.generativeai as genai
import tweepy

# Configure the API keys securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Twitter API configuration
twitter_api_key = st.secrets["TWITTER_API_KEY"]
twitter_api_secret = st.secrets["TWITTER_API_SECRET"]
twitter_access_token = st.secrets["TWITTER_ACCESS_TOKEN"]
twitter_access_token_secret = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]

twitter_auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
twitter_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(twitter_auth)

# Streamlit App UI
st.title("Ever AI")
st.write("Use generative AI to get responses based on your prompt.")

# Prompt input field
prompt = st.text_input("Enter your prompt:", "Best alternatives to javascript?")

# Button to generate response
if st.button("Generate Response"):
    try:
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model
        response = model.generate_content(prompt)
        
        # Display response in Streamlit
        st.write("Response:")
        st.write(response.text)
        
        # Twitter sharing button
        if st.button("Tweet"):
            tweet = response.text[:280]  # Truncate response to 280 characters
            twitter_api.update_status(status=tweet)
            st.success("Tweeted!")
    except Exception as e:
        st.error(f"Error: {e}")
