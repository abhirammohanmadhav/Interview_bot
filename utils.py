from nltk.metrics import edit_distance
from nltk.metrics import jaccard_distance
import nltk
import pyttsx3
import speech_recognition as sr
import openai
from typing import List, Optional, Union, Any

class InterviewAssistant:
    def __init__(self):
        """Initialize the InterviewAssistant
        """
        self.engine = pyttsx3.init()

    def generate_interview_questions(self, job_description: str, num_questions: int) -> List: 
        """Generates interview questions keeping the job description as a reference

        Args:
            job_description (str): job description 
            num_questions (int): number of questions that the chatbot should ask

        Returns:
            list(str): list of questions generated by a bot
        """
        prompt = "Generate {} interview questions based on the following job description:\n\n".format(num_questions) + job_description + "\n\nQuestions:"
        params = {
            "model": "gpt-3.5-turbo",
            "messages":[{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.5,
            "stop": ["\n"],
            "n": num_questions
        }
        response = openai.ChatCompletion.create(**params)
        questions = [choice['message']['content'] for choice in response['choices']]
        return questions

    def generate_answers(self, question:str) -> List:
        """Generates answers for the respective questions

        Args:
            question (str): generated question

        Returns:
            list(str): list of answers for the particular list of questions
        """
        prompt = "Answer the following interview question:\n\n" + question + "\n\nAnswer:"
        params = {
            "model": "gpt-3.5-turbo",
            "messages":[{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0.5,
            "stop": ["\n"],
        }
        response = openai.ChatCompletion.create(**params)
        answers = [choice['message']['content'] for choice in response['choices']]
        return answers

    def calculate_jaccard_similarity(self, candidate_answer:str, ideal_answer:str) -> float:
        """Measure of similarity between two sets. J(A, B) = |A Intersection B|/|A Union B|

        Args:
            candidate_answer (str): Answer from the candidate
            ideal_answer (str): Answer generated by the chatbot

        Returns:
            float: Value of jaccard similarity
        """
        candidate_tokens = set(nltk.word_tokenize(candidate_answer.lower()))
        ideal_tokens = set(nltk.word_tokenize(ideal_answer.lower()))
        return 1 - jaccard_distance(candidate_tokens, ideal_tokens)

    def calculate_levenshtein_similarity(self, candidate_answer:str, ideal_answer:str) -> float:
        """Calculated the levenshtein similarity - measures the minimum number of single-character edits 
        (insertions, deletions, or substitutions) required to change one string into another. 
        L(A, B) = distance(A, B)/max(|A|,|B|)

        Args:
            candidate_answer (str): answer given by the candidate
            ideal_answer (str): answer generated by the chatbot

        Returns:
            float: Levenshtein similarity
        """
        return 1 / (edit_distance(candidate_answer.lower(), ideal_answer.lower()) + 1)

    def ask_question(self, question:str):
        """Generates a voice for the question given

        Args:
            question (str): the quesiton that the model generated
        """
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[2].id)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('pitch', 50)
        self.engine.say(question)
        self.engine.runAndWait()

    def get_audio(self):
        """Recieves the audio answer from the candidate
        """
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            response = recognizer.recognize_google(audio)
            print("You said:", response)
            return response
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
