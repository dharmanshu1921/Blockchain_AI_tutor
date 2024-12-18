#!/usr/bin/env python
import sys
import warnings
import speech_recognition as sr
from crew import BlockchainTutorCrew
from PIL import Image
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_text_query():
    """
    Get query input from the user via text.
    """
    return input("Enter your blockchain-related query: ")

def get_audio_query():
    """
    Get query input from the user via audio using speech recognition.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    print("Listening... Please speak your blockchain-related query.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  
        audio = recognizer.listen(source)
    
    try:
        query = recognizer.recognize_google(audio)
        print(f"Detected query: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio. Please try again.")
    except sr.RequestError as e:
        print(f"Speech Recognition API error: {e}")
    return None

def get_image_query():
    """
    Get query input from the user via image.
    """
    image_path = input("Enter the path to the image file: ").strip()
    try:
        image = Image.open(image_path)
        print("Image loaded successfully.")
        return image
    except Exception as e:
        print(f"Failed to load the image: {e}")
        return None

def run():
    """
    Run the Blockchain AI Tutor crew.
    """
    print("Welcome to the Blockchain AI Tutor!")
    print("Choose input method:")
    print("1. Text")
    print("2. Audio")
    print("3. Image")
    choice = input("Enter your choice (1 or 2): ").strip()
    
    # Initialize query variable
    query = None
    
    if choice == "1":
        query = get_text_query()
    elif choice == "2":
        query = get_audio_query()
        if not query: 
            print("Switching to text input due to audio error.")
            query = get_text_query()
    elif choice == "3":
        image = get_image_query()
        if not image:
            print("Image input failed. Exiting.")
            return
        inputs = {'image': image}
    else:
        print("Invalid choice. Defaulting to text input.")
        query = get_text_query()

    if query:
        search_input = query  # Directly pass the query as a string
        crew_instance = BlockchainTutorCrew().crew()
        result = crew_instance.kickoff(inputs={'search_query': search_input})  # Pass the query as a string
        print(f"Result: {result}")

if __name__ == "__main__":
    run()
