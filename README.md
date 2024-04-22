# Interview_bot

Run the "interview_bot.py" python script by providing the job description file path (for this example I have used a text file), name of the bot that you would like to keep, number of questions that the bot should ask and the threshold for the decision making by the bot, to the main() function. Also you would have to update the OPENAI_API_KEY.

In this interview bot I have used GPT-3.5-turbo model, from OpenAI which generates the questions based on the job description and also generates its own answers. Upon comparison between the user response and the generated answer, it makes a decision whether to hire the candidate or not. 