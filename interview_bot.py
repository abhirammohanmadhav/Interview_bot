import numpy as np
from utils import InterviewAssistant
import openai
import os
from pathlib import Path
from typing import Union

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def main(mode_of_interview:str, threshold:float, jd_file_path:Union[str, Path], num_questions:int, bot_name:str):
    """This is the main function where the chatbot runs on the terminal. It has the option of incorporating
    voice or chat mode.

    Args:
        mode_of_interview (str): Can choose between a voice bot or a chat bot
        threshold (float): Manually set to make a decision whether to hire a candidate or not
        jd_file_path (Union[str, Path]): path to the job description in the form of question and answer
        num_questions (int): The number of questions that the chatbot needs to ask 
    """

    if os.path.exists(jd_file_path):
        with open(jd_file_path, "r") as f:
            job_description = f.read()

    assistant = InterviewAssistant()    

    question_prompts = assistant.generate_interview_questions(job_description, num_questions)

    print(f"\nHi!, I am {bot_name}. I will be your interviewer today.")
    print("Welcome to the interview for the position of OpenAI Technical Expert / Data Scientist!")
    print("Thank you for taking your time to interview with us.\n\n")

    coherence_scores = []
    coherence_score = 0
    current_question_index = 0
    jaccard_similarities = []
    levenshtein_similarities = []

    if mode_of_interview == "voice":
        question = "Can you please introduce yourself?"
        assistant.ask_question(question)
        assistant.get_audio()
        assistant.ask_question("Thats great!, let us start the interview")

        # Display questions one at a time and get user responses
        while current_question_index < len(question_prompts):

            assistant.ask_question(question_prompts[current_question_index])
            user_response = assistant.get_audio()

            # Check if the user has provided a response
            if user_response.strip():
                # Calculate coherence score for the current question
                ideal_answer = assistant.generate_answers(question_prompts[current_question_index])
                jaccard_similarity = assistant.calculate_jaccard_similarity(user_response, ideal_answer[0])
                levenshtein_similarity = assistant.calculate_levenshtein_similarity(user_response, ideal_answer[0])
                jaccard_similarities.append(jaccard_similarity)
                levenshtein_similarities.append(levenshtein_similarity) 
                coherence_score = np.mean(max(jaccard_similarities) + max(levenshtein_similarities))

                print(f"Coherence score for question {current_question_index + 1}: {coherence_score}")          
                coherence_scores.append(coherence_score)

                # Increment current question index
                current_question_index += 1

    elif mode_of_interview == "chat":
        print(f"{bot_name}: Can you please introduce yourself?")
        print(input(f"You: "))
        print(f"{bot_name}: Thats great!, let us start the interview")

        # Display questions one at a time and get user responses
        while current_question_index < len(question_prompts):
            print(f"Bot: {question_prompts[current_question_index]}")
            user_response = input(f"You: ")

            # Check if the user has provided a response
            if user_response.strip():
                # Calculate coherence score for the current question
                ideal_answer = assistant.generate_answers(question_prompts[current_question_index])
                # for answer in ideal_answer:
                jaccard_similarity = assistant.calculate_jaccard_similarity(user_response, ideal_answer[0])
                levenshtein_similarity = assistant.calculate_levenshtein_similarity(user_response, ideal_answer[0])
                jaccard_similarities.append(jaccard_similarity)
                levenshtein_similarities.append(levenshtein_similarity) 

                coherence_score = np.mean(max(jaccard_similarities) + max(levenshtein_similarities))
                # Print the coherence score for the current question
                print(f"Coherence score for question {current_question_index + 1}: {coherence_score}")          
                coherence_scores.append(coherence_score)

                # Increment current question index
                current_question_index += 1


    # Make hiring decision based on mean coherence score
    mean_coherence_score = sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0
    print(mean_coherence_score, coherence_scores)
    if mean_coherence_score >= threshold:  # Adjust threshold as needed
        print("Congratulations! We are glad to make you an offer.")
    else:
        print("Thank you for the interview. However, we are not able to select you at this moment.")

if __name__ == "__main__":

    mode_of_interview = "voice"
    threshold = 0.7
    JD_file_path = r"C:\D\applications\deutsch\Tüv\Interview_use_case\Interview_Bot\Q_and_A.txt"
    num_questions = 5
    bot_name = "Linda"

    main(mode_of_interview, threshold, JD_file_path, num_questions, bot_name)
