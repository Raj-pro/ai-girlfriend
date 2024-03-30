import tkinter as tk
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr

class ChatRoom:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Room")

        self.text_area = tk.Text(self.root)
        self.text_area.pack()

        self.listen_button = tk.Button(self.root, text="Press to Speak", command=self.listen_and_send)
        self.listen_button.pack(pady=20)

        # Set up the model
        genai.configure(api_key="API_KEY")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
       
        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                           generation_config=generation_config)
        self.convo = self.model.start_chat(history=[])

    def listen_and_send(self):
        # Initialize the recognizer
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            # Convert audio to text
            msg = recognizer.recognize_google(audio)
            print("You said:", msg)

            # Add user message to the chat history
            self.text_area.insert(tk.END, "User : " + msg + '\n\n')

            # Send the message to the model and get the response
            self.convo.send_message(msg+"(this is send by boyfriend to his girlfriend . As a girlfriend, how would you respond to your boyfriend in 20 word with 1 face imoji and 1 hand imoji?)")
            response = self.convo.last.text

            # Display the model's response
            self.text_area.insert(tk.END, "Gemini : " + response + '\n\n')

            # Speak out the response
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say(response)
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

root = tk.Tk()
chat_room = ChatRoom(root)
root.mainloop()
