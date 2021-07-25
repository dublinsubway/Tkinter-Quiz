import tkinter as tk #import tkinter for gui
import sqlite3 #sql module for database
from web_scraper import QuestionsAndAnswers #webscraped Questions and Answers

conn = sqlite3.connect('quiz.db') #connect to database
cursor = conn.cursor() #cursor for executing sql
#create table Users if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
  username text PRIMARY KEY,
  password text NOT NULL,
  score int DEFAULT 0
)''')
#quiz app class
# We used the code from this stackoverflow answer to get an idea of how our tkinter screens/frames should work
#https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
class QuizApp(tk.Tk): 
  
  # __init__ function for class QuizApp 
  def __init__(self, *args, **kwargs): 
    
    # __init__ function for class Tk
    tk.Tk.__init__(self, *args, **kwargs)
    
    # creating a MainFrame
    MainFrame = tk.Frame(self) 
    MainFrame.pack(side = "top") 

    MainFrame.grid_rowconfigure(0, weight = 1)
    MainFrame.grid_columnconfigure(0, weight = 1)
    # initializing frames to an empty array
    self.frames = {} 

    # iterating through a tuple consisting
    # of the different page layouts
    for F in (StartPage, Login, Register, Logged_in, Leaderboard):

      frame = F(MainFrame, self)

      self.frames[F] = frame 

      frame.grid(row = 0, column = 0, sticky ="nsew")

    self.show_frame(StartPage)

  # to display the current frame passed as
  # parameter
  def show_frame(self, cont):
    frame = self.frames[cont]
    frame.tkraise()
    frame.event_generate("<<ShowFrame>>")

# first window frame startpage

class StartPage(tk.Frame):
  def __init__(self, parent, controller): 
    tk.Frame.__init__(self, parent, width=600, height=330)
    self.controller = controller

    heading_label = tk.Label(self, text ="Main Menu",bg="#34eb9e", width="30", height="2", font=("Calibri", 13))
    
    heading_label.place(x=300, y=25, anchor="center")

    login_screen_button = tk.Button(self, text ="Login", height="2", width="30", bg="#05def2",
    command = lambda : controller.show_frame(Login))

    login_screen_button.place(x=300, y=90, anchor="center")

    register_screen_button = tk.Button(self, text ="Register", height="2", width="30", bg="#05def2",
    command = lambda : controller.show_frame(Register))

    register_screen_button.place(x=300, y=140, anchor="center")

    guest_screen_button = tk.Button(self, text ="Guest", height="2", width="30", bg="#05def2",
    command = lambda : self.guest())

    guest_screen_button.place(x=300, y=190, anchor="center")

  def guest(self):
    global username1
    username1 = None
    self.controller.show_frame(Logged_in)

# Login Frame
class Login(tk.Frame):
  
  def __init__(self, parent, controller):
    self.controller = controller
    tk.Frame.__init__(self, parent)
    heading_label = tk.Label(self, text ="Login Page", bg="#34eb9e", width="30", height="2", font=("Calibri", 13))
    heading_label.place(x=300, y=25, anchor="center")
    
    username_label = tk.Label(self, text ="username:", height="1", font=("Calibri", 12))
    username_label.place(x=300, y=80, anchor="center")
    self.username = tk.Entry(self)
    self.username.place(x=300, y=100, anchor="center")
    password_label = tk.Label(self, text ="password:", height="1", font=("Calibri", 12))
    password_label.place(x=300, y=140, anchor="center")
    self.password = tk.Entry(self)
    self.password.place(x=300, y=160, anchor="center")

    back_button = tk.Button(self, text ="Back",
              command = lambda : controller.show_frame(StartPage), padx=10, pady=2, fg="white", 
              bg="#263D42", font="Helvetica 10 bold")

    back_button.place(x=140, y=230, anchor="center")

    login_button = tk.Button(self, text ="Submit",
              command = self.Login_attempt, padx=10, pady=2, fg="white", 
              bg="#263D42", font="Helvetica 16 bold")
  
    login_button.place(x=300, y=220, anchor="center")

  def Login_attempt(self):
    '''function to check login credentials are correct'''
    self.user = self.username.get().lower() #username entered
    self.password1 = self.password.get() #password entered
    global username1
    username1 = self.user
    cursor.execute("SELECT * FROM USERS WHERE username LIKE ?", (self.user,)) #find user in database
    user_data = cursor.fetchone() #store user data in variable
    if user_data is None: #if user doesn't exist in database
      user_doesnt_exist = tk.Label(self,text="Username incorrect: please try again or register") #create label for username incorrect
      user_doesnt_exist.place(x=300, y=300, anchor="center") #display label
    else: #user exists in database
      password_stored = user_data[1] #get password for user
      if self.password1 == password_stored: #password stored in db matches password entered
        self.controller.show_frame(Logged_in) #call logged in function
      else: #password entered is incorrect
        wrong_password = tk.Label(self,text="Password incorrect") #create label for username incorrect
        wrong_password.place(x=300, y=300, anchor="center") #display label

class Register(tk.Frame): 
  def __init__(self, parent, controller):
    self.controller = controller
    tk.Frame.__init__(self, parent)
    heading_label = tk.Label(self, text ="Registration Page", bg="#34eb9e", width="30", height="2", font=("Calibri", 13))
    heading_label.place(x=300, y=25, anchor="center")
    
    username_label = tk.Label(self, text ="username:", height="1", font=("Calibri", 12))
    username_label.place(x=300, y=80, anchor="center")
    self.username = tk.Entry(self)
    self.username.place(x=300, y=100, anchor="center")

    password_label = tk.Label(self, text ="password:", height="1", font=("Calibri", 12))
    password_label.place(x=300, y=140, anchor="center")
    self.password = tk.Entry(self)
    self.password.place(x=300, y=160, anchor="center")

    back_button = tk.Button(self, text ="Back",
              command = lambda : controller.show_frame(StartPage), padx=10, pady=2, fg="white", 
              bg="#263D42", font="Helvetica 10 bold")

    back_button.place(x=140, y=230, anchor="center")

    register_button = tk.Button(self, text ="Submit",
              command = self.Register_attempt, padx=10, pady=2, fg="white", 
              bg="#263D42", font="Helvetica 16 bold")
  
    register_button.place(x=300, y=220, anchor="center")

  def Register_attempt(self):
    self.user = self.username.get().lower() #username entered
    self.password1 = self.password.get() #password entered
    global username1
    username1 = self.user
    if len(self.user) < 3:
      username_short = tk.Label(self,text="Username too short")
      username_short.place(x=300, y=300, anchor="center")
    elif len(self.password1) < 6:
      password_short = tk.Label(self,text="Password too short")
      password_short.place(x=300, y=300, anchor="center")
    else:
      cursor.execute("SELECT * FROM USERS WHERE username LIKE ?", (self.user,)) #find user in database
      user_data = cursor.fetchone() #store user data in variable
      if user_data is None: #if user doesn't exist in database
        cursor.execute('''INSERT INTO USERS (username,password) values (?, ?)''',(self.user,self.password1))
        conn.commit()
        self.controller.show_frame(Logged_in)
      else: #user exists in database
        user_exists = tk.Label(self,text="Username already exists")
        user_exists.place(x=300, y=300, anchor="center")

class Logged_in(tk.Frame): 
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    self.question_label = tk.Label(self, text ="",wraplength=300, bg="#f22470", width=30, height=3, font="Helvetica 12 bold")
    self.question_label.place(x=300, y=25, anchor="center")
    self.Questions = list(QuestionsAndAnswers.keys())
    self.question_number = -1 #set question number to -1
    self.question_from_list = "" #set question from list of questions to empty string
    self.submit = tk.Button(self, text ="Submit",
              command = self.submitted, padx=10, pady=2, fg="white", 
              bg="#263D42", font="Helvetica 16 bold")
    self.submit.place(x=300, y=220, anchor="center")
    self.user_answer = tk.Entry(self, width=30, bg="black", fg="white", borderwidth="5", font="Helvetica 16 bold", justify="center") #create entry box for users answer
    self.user_answer.place(x=300, y=160, anchor="center") #display entry box
    self.score = 0 #sets score to 0 at start
    self.wrong = [] #sets empty list for questions answered incorrectly
    self.question()

  def question(self): #used to go through questions list and display each question followed by results
    if self.question_number < len(self.Questions) -1: #checks if all questions have been asked
      self.question_number += 1 #adds to question number each timw question is asked
      self.question_from_list = self.Questions[self.question_number] #gets next question from list
      self.question_label.config(text=self.question_from_list) #sets question label to next question
    else: #all questions in list asked
      self.result()

  def submitted(self):
    my_answer = self.user_answer.get() #gets answer entered by user
    if my_answer.upper() == QuestionsAndAnswers[self.question_from_list].upper(): #if answer entered by user is correct
      self.score += 1 #add 1 to score
    else: #answer entered is incorrect
      self.wrong.append(self.question_from_list) #add question to wrong list
    submissionLabel = tk.Label(self, text="Answer Submitted!") #label with text answer submitted
    submissionLabel.place(x=300, y=300, anchor="center") #display label
    submissionLabel.after(1000, lambda:submissionLabel.destroy()) #destroy label after 1 second
    self.user_answer.delete(0, tk.END) #empty user answer entry box
    self.question() #call question finction again

  def result(self):
    self.user_answer.destroy()
    self.submit.destroy()
    if username1 is not None: #not guest
      cursor.execute("SELECT * FROM USERS WHERE username LIKE ?", (username1,))
      user_data = cursor.fetchone()
      if int(user_data[2]) < self.score:
        cursor.execute("UPDATE USERS SET score = ? WHERE username LIKE ?", (self.score,username1,))
        conn.commit()
    result = "you got " + str(self.score) + "/" + str(len(self.Questions)) + " correct" #displays user score
    self.question_label.config(text=result, bg="green") #changes question label text to result
    self.question_label.grid(row=0, column=1, pady=1) #displays question label
    Incorrect_label = tk.Label(self, text="Answered incorrectly:", bg="purple", width=20, height=1, font="Helvetica 14 bold", padx=0, pady=1) #incorrectly answered text label
    Incorrect_label.grid(row=2, column=1) #displays label
    Leaderboard_button = tk.Button(self, text="Leaderboard", bg="#05def2", fg="black", command= lambda: self.controller.show_frame(Leaderboard))
    Leaderboard_button.place(x=700, y=80, anchor="e")
    i = 2 #sets row number to display each question answered incorrectly
    for wrong_answer in self.wrong: #goes through list of wrong answers
      i +=1 #adds 1 to row number for each question
      solution = wrong_answer + " " + QuestionsAndAnswers[wrong_answer] #sets solution to question and answer
      correct_answer = tk.Label(self, text=solution, bg="red", width=80, height=1, font="Helvetica 12 bold") #sets label for solution
      correct_answer.grid(row=i, column=1, padx=10, pady=1) #displays label

class Leaderboard(tk.Frame): 
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.bind("<<ShowFrame>>", self.on_show_frame)

  def on_show_frame(self, event):
    cursor.execute("SELECT * FROM USERS") #find user in database
    user_data = cursor.fetchall() #store user data in variable
    heading_label = tk.Label(self, text ="Leaderboard", bg="red", width=30, height=3, font="Helvetica 12 bold")
    heading_label.place(x=430, y=25, anchor="center")
    col_title = tk.Label(self, text ="Username Highscore", bg="blue", fg="white", width=30, height=3, font="Helvetica 12 bold")
    col_title.place(x=430, y=90, anchor="center")
    i = 115
    for user in user_data:
      user, password, score = user
      i +=20
      user_score = tk.Label(self, text=user + " " + str(score), bg="red", width=30, height=1, font="Helvetica 12 bold") #sets label for solution
      user_score.place(x=430, y=i, anchor="center") #displays label

app = QuizApp()
app.title("Quiz")
app.mainloop()
