import streamlit as st
from PIL import Image
import os
from google import genai
from io import BytesIO

def main():
    st.set_page_config(page_title="Tinder Gen App", page_icon=":tada:", layout="wide")
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
            st.warning("Click the 'Generate Image' button to generate an image.")
        else:
            if not prompt:
                st.error("Please enter a prompt to generate an image.")
            if not uploaded_image:
                st.error("Please upload an image to generate a transformation.")
            if not api_key:
                st.error("Please enter your API key to generate an image.")
                
            try:
                with st.spinner("Generating image..."):
                    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
                    response = client.models.generate_content(
                      model="gemini-2.5-flash-image-preview",
                      contents=[prompt, uploaded_image]
                    )
                    
                    if response:
                        image_parts = [
                            part.inline_data.data
                            for part in response.candidates[0].content.parts
                            if part.inline_data
                        ]
                        
                        if image_parts:
                            image = Image.open(BytesIO(image_parts[0]))
                            st.image(image, caption="Generated Image", width="stretch")
                        else:
                            st.error("Failed to generate image. Please try again.")
                    else:
                      st.error("Failed to generate image. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}") 
                        

if __name__ == "__main__":
    main()
