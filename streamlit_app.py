import streamlit as st
import google.generativeai as genai
import tweepy

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Twitter API configuration
twitter_auth = tweepy.OAuthHandler(st.secrets["TWITTER_API_KEY"], st.secrets["TWITTER_API_SECRET_KEY"])
twitter_auth.set_access_token(st.secrets["TWITTER_ACCESS_TOKEN"], st.secrets["TWITTER_ACCESS_TOKEN_SECRET"])
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit=True)

# Streamlit App UI
st.title("Ever AI")
st.write("Use generative AI to get responses based on your prompt.")

# Prompt input field
prompt = st.text_input("Enter your prompt:", "Best alternatives to JavaScript?")

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
        
        # Option to post the response to Twitter
        if st.button("Post to Twitter"):
            try:
                tweet = response.text
                twitter_api.update_status(status=tweet)
                st.success("Tweet posted successfully!")
            except tweepy.TweepError as e:
                st.error(f"Error posting to Twitter: {e}")
                st.error(f"Twitter API response: {e.response.text}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
