import streamlit as st
from PIL import Image
import os
from google import genai
from io import BytesIO
import re
from mailerlite.client import Client


def add_to_mailerlite(email):
    try:
        mailerlite_api_key = st.secrets["MAILERLITE_API_KEY"]
        mailerlite_group_id = st.secrets["MAILERLITE_GROUP_ID"]
        
        client = Client({
            "api_key": mailerlite_api_key
        })
        
        client.subscribers.create(email, resubscribe=True, groups=[mailerlite_group_id])
        st.success("You have been subscribed!")
    except Exception as e:
        st.error(f"An error occurred while subscribing: {e}")


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
