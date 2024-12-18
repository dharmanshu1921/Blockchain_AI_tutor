import streamlit as st
from PIL import Image
from crew import BlockchainTutorCrew
import speech_recognition as sr

# Set up Streamlit app configuration
st.set_page_config(
    page_title="Blockchain AI Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Blockchain AI Tutor Crew
crew = BlockchainTutorCrew().crew()

# App Title and Description
st.title("🧠 Blockchain AI Tutor")
st.markdown(
    """
    Welcome to the **Blockchain AI Tutor**! 🚀  
    This AI-powered tutor can help you with blockchain-related questions using:
    - **Text Input**
    - **Audio Input**
    - **Image Input**  
    Select your preferred input method from the sidebar and start exploring!
    """
)

# Sidebar for Input Selection
st.sidebar.header("Choose Input Method")
input_method = st.sidebar.radio(
    "How would you like to input your query?",
    options=["Text", "Audio", "Image"]
)

# Helper Functions
def process_text_query(query):
    """
    Process text input and prepare for the AI Tutor.
    """
    st.info(f"Processing your text query: {query}")
    return {"query": query}

def process_audio_query():
    """
    Record and process an audio input query.
    """
    recognizer = sr.Recognizer()
    st.info("Listening for your query...")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        query = recognizer.recognize_google(audio)
        st.success(f"Audio recognized: {query}")
        return {"query": query}
    except sr.UnknownValueError:
        st.error("Sorry, we could not understand your audio. Please try again.")
    except sr.RequestError as e:
        st.error(f"Speech Recognition error: {e}")
    return None

def process_image_query(image_file):
    """
    Process an uploaded image input query.
    """
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    return {"image": image}

# Handle User Input
inputs = None

if input_method == "Text":
    text_query = st.text_input("Enter your blockchain-related query:")
    if st.button("Submit Text Query"):
        if text_query:
            inputs = process_text_query(text_query)
        else:
            st.warning("Please enter a query before submitting.")

elif input_method == "Audio":
    if st.button("Record Audio Query"):
        try:
            inputs = process_audio_query()
        except Exception as e:
            st.error(f"Audio input failed: {e}")

elif input_method == "Image":
    image_file = st.file_uploader("Upload an image file (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])
    if image_file:
        if st.button("Submit Image Query"):
            inputs = process_image_query(image_file)

# Process Query with Blockchain AI Tutor
if inputs:
    with st.spinner("Processing your query with the Blockchain AI Tutor..."):
        try:
            result = crew.kickoff(inputs=inputs)
            st.success("🎉 Blockchain AI Tutor Response:")
            st.markdown(f"**{result}**")
        except Exception as e:
            st.error(f"An error occurred while processing your request: {e}")
