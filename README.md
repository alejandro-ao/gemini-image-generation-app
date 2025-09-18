# Tinder-Gen-App

This repository contains the code for an image generation application themed as a Tinder photo generator. This project is for educational purposes and accompanies a tutorial on YouTube.

**YouTube Tutorial:** https://youtu.be/WLuYhBesLiI
**Live Application:** tinder-image-gen.app

## Purpose

This application is designed to demonstrate how to build an image generation app using Python. The user interface is built with Streamlit, and it uses Google's Gemini 2.5 Flash (Nano Banana) for image generation based on a prompt. It is intended to remain exactly as it was presented in the tutorial and does not accept contributions.

## How to Run

You can run this application using either `uv` or `pip`.

### Using UV

If you have `uv` installed, you can run the application with the following command:

```bash
uv run streamlit run main.py
```

### Using Pip

If you prefer to use `pip`, you will need to create a virtual environment and install the dependencies from the `requirements.txt` file.

1.  Create a virtual environment:

    ```bash
    python -m venv .venv
    ```

2.  Activate the virtual environment:

    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Run the application:

    ```bash
    streamlit run main.py
    ```

## Disclaimer

This repository is for educational purposes only and does not accept contributions. The code is intended to remain exactly as it was presented in the tutorial. If you want to use this app without the need to create your own Google Developer account and API keys, you can run it at [tinder-image-gen.app](https://tinder-image-gen.app).