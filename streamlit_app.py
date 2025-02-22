import streamlit as st
import google.generativeai as genai
import tweepy
import hashlib
import os

# Configure the API keys securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Twitter API configuration
twitter_api_key = st.secrets["TWITTER_API_KEY"]
twitter_api_secret = st.secrets["TWITTER_API_SECRET_KEY"]
twitter_access_token = st.secrets["TWITTER_ACCESS_TOKEN"]
twitter_access_token_secret = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]

twitter_auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
twitter_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(twitter_auth)

# User authentication
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

def register_user(username, password):
    stored_password = hash_password(password)
    with open("users.txt", "a") as f:
        f.write(f"{username}:{stored_password}\n")

def login_user(username, password):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f.readlines():
            stored_username, stored_password = line.strip().split(":")
            if stored_username == username and check_password(stored_password, password):
                return True
    return False

# Streamlit App UI
st.title("Ever AI")

# User authentication
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if login_user(login_username, login_password):
                st.session_state.username = login_username
            else:
                st.error("Invalid username or password")

    with register_tab:
        register_username = st.text_input("Username", key="register_username")
        register_password = st.text_input("Password", type="password", key="register_password")
        if st.button("Register", key="register_button"):
            if not os.path.exists("users.txt"):
                open("users.txt", "w").close()
            register_user(register_username, register_password)
            st.success("User registered successfully")
else:
    # App functionality
    st.write(f"Welcome, {st.session_state.username}!")

    # Prompt input field
    prompt = st.text_input("Enter your prompt:", "Best alternatives to javascript?", key="prompt_input")

    # Button to generate response
    if st.button("Generate Response", key="generate_response_button"):
        try:
            # Load and configure the model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Generate response from the model
            response = model.generate_content(prompt)
            
            # Display response in Streamlit
            st.write("Response:")
            st.write(response.text)
            
            # Twitter sharing button
            if st.button("Tweet", key="tweet_button"):
                try:
                    tweet = response.text[:280]  # Truncate response to 280 characters
                    twitter_api.update_status(status=tweet)
                    st.success("Tweeted!")
                except tweepy.TweepError as e:
                    st.error(f"Error tweeting: {e}")
                except Exception as e:
                    st.error(f"Error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")
