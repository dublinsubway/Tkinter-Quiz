#!/usr/bin/env python3
import random
import requests #import requests module
from bs4 import BeautifulSoup #import beautiful soup module

topics = ["actors","art", "australia", "biology", "dinosaurs",
"economy", "film", "food", "vegetables", "general-knowledge",
"geography", "history", "informatics", "language",  "literature",
"music", "nature", "politics", "science", "sports"]
# subject = topics[random.randint(0,19)]
# print(subject)
subject = "general-knowledge" #set subject of quiz
URL = "https://www.quiz-questions.net/" + subject + ".php" #url of quiz questions

page = requests.get(URL, "lxml") #get website data
questions =[] #empty questions list

soup = BeautifulSoup(page.content, "html.parser") #parse html
for question in soup.find_all("td"): #get all questions from table
  if question.text[0].isdigit() and "?" in question.text: #isolate questions by selecting lines starting with a question number that include a question mark
    questions.append(question.text.strip()) #add question to questions list

QuestionsAndAnswers = {} #create empty questions and asnwers dictionary
for question in questions: #go through all questions in list
  question = question.lstrip("0123456789") #remove number from start of question
  quest_and_ans = question.split("?") #seperate question and answer
  QuestionsAndAnswers[quest_and_ans[0] + "?"] = quest_and_ans[1] #add question and answer to dictionary

if __name__ == "__main__": #if webscraper is run directly
  for question, answer in QuestionsAndAnswers.items(): #go through every question and answer in dictionary
    print(question, answer) #print question and answer
    print(QuestionsAndAnswers)
