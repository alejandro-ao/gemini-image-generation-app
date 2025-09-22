import streamlit as st
from PIL import Image
import os
from google import genai
from io import BytesIO
import re
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_to_mailerlite(email):
    try:
        mailerlite_api_key = st.secrets["MAILERLITE_API_KEY"]
        mailerlite_group_id = st.secrets["MAILERLITE_GROUP_ID"]
        logging.info(f"Attempting to subscribe {email} to group {mailerlite_group_id}")

        url = "https://connect.mailerlite.com/api/subscribers"
        headers = {
            "Authorization": f"Bearer {mailerlite_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "email": email,
            "groups": [str(mailerlite_group_id)],
            "resubscribe": True
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        st.success("You have been subscribed!")
        logging.info(f"Successfully subscribed {email}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error subscribing {email}: {e}", exc_info=True)
        st.error(f"An error occurred while subscribing: {e.response.text}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        st.error("An unexpected error occurred while subscribing.")


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def get_session_state():
    if "email_submitted" not in st.session_state:
        st.session_state.email_submitted = False


def main():
    get_session_state()
    st.set_page_config(page_title="Tinder Gen App", page_icon=":fire:", layout="wide")

    if not st.session_state.email_submitted:
        st.title("🔥 Tinder Gen App")
        st.write("Welcome to the Tinder Gen App!")
        st.header("Enter your email to access the app")
        with st.form(key="email_form"):
            email = st.text_input("Email Address")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                if is_valid_email(email):
                    add_to_mailerlite(email)
                    st.session_state.email_submitted = True
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
    else:
        st.title("🔥 Tinder Gen App")
        st.write("Welcome to the Tinder Gen App!")
        
        with st.sidebar:
            st.header("Settings")
            api_key = st.text_input(
                "Enter your API key",
                type="password",
                key="api_key"
            )
            if api_key:
                os.environ["GOOGLE_API_KEY"] = api_key
                st.success("API key saved!")
            else:
                st.warning("Please enter your API key to use this app.")
                
        
        prompt = st.text_area(
            "Enter your prompt",
            placeholder="Describe how you want to transform or generate the image for your Tinder profile.",
            height=200,
            key="prompt_input"
        )
        
        uploaded_image = st.file_uploader(
            "Upload image",
            type=["jpg", "jpeg", "png"],
            key="uploaded_image"
        )
        
        generate_button = st.button(
            "Generate Image",
            key="generate_button",
            use_container_width=True,
            type="primary",
        )
        
        col1, col2 = st.columns(2)
        
        with col1: 
            st.header("Uploaded Image")
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image", width="stretch")
          
        with col2:
            st.header("Generated Image")
            if not generate_button:
                st.write("Click the 'Generate Image' button to generate an image.")
            else: 
                try:
                    with st.spinner("Generating image..."):
                        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
                        image = Image.open(uploaded_image)
                        response = client.models.generate_content(
                            model="gemini-2.5-flash-image-preview",
                            contents=[prompt, image]
                        )
                        image_parts = [
                          part.inline_data.data
                          for part in response.candidates[0].content.parts
                          if part.inline_data
                        ]
                        if image_parts:
                            image = Image.open(BytesIO(image_parts[0]))
                            st.image(image, caption="Generated Image", width="stretch")
                        else:
                            st.error("Failed to generate image.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
