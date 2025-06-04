import os
import chainlit as cl
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI client to use Google API key and Gemini endpoint
openai.api_key = os.getenv("GOOGLE_API_KEY")
openai.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Assign the openai module as the client for API calls
client = openai
# Alternative: Use OpenAI(api_key=api_key, base_url=base_url) if available

@cl.on_message
async def handle_message(message: cl.Message):
    """
    Event handler for incoming messages from the user.
    Receives user input, sends it to the Gemini model for translation,
    and returns the translated text.
    """
    user_input = message.content
    # Construct the prompt for translation
    prompt = f"Translate this to the target language user asks for:\n\n{user_input}"

    try:
        # Call the Gemini model using the OpenAI-compatible API
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract the translated text from the response
        translated_text = response.choices[0].message.content
        # Send the translated text back to the user
        await cl.Message(content=translated_text).send()

    except Exception as e:
        # Handle and report any errors during the API call
        await cl.Message(content=f"Error: {str(e)}").send()
