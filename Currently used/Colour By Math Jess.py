#########################
##                     ##
##    Colour by Math   ##
##                     ##
#########################

#Import tkinter library for GUI as well as time & random libraries.
from tkinter import *
import time
import random

#Setting up the base colour palette for easier reference
YELLOW = '#fff200'
DUSTY_BLUE = '#7092be'

MINIMUM_AGE = 5
MAXIMUM_AGE = 10

#Class for the main window (window one)
class window_one:
    #Initialize values for window_one class
    def __init__(self):
        canvas.bind("<Button-1>", self.left_clicked) #Bind the left click button to the canvas
        main_window.bind("<Return>",self.return_pressed) #Bind the return key to the window
        validation = main_window.register(self.only_numbers) #Initialise validation command
        #Sets up/Initialises a entry box for the authorise page that checks whether the characters entered are integers
        self.age_entry=Entry(main_window, justify = RIGHT, validate = "key", validatecommand = (validation,'%S'))
        #Sets up/Initialises a entry box for the picture entry box that checks whether the characters entered are integers
        self.picture_entry=Entry(main_window, justify = RIGHT, validate = "key", validatecommand = (validation,'%S'))
        #Initialises a button that checks whether the entered number is right
        self.check_button = Button(main_window,  text = "Check", font="Arial 14", bg = DUSTY_BLUE, width=7,command=self.written_option)
        #Initialises a button that checks whether the entered number is between required values
        self.enter_button = Button(main_window,  text = "Check", font="Arial 14", bg = DUSTY_BLUE, width=7,command=self.age_check)
        
    
    def quit(self):          #Quit the program
        main_window.destroy()#Closes the window

    #Load the game after pressing start button 
    def start(self):
        print("Start program here")#Print a cue in shell for testing and developer purposes
        object_list.clear() #Clear the objects list
        csv_objects('authorise_env.csv') #Load the environment for the game using the csv_objects subroutine
        canvas.create_window(400, 300, window = self.age_entry) #Create a window for the entry box
        canvas.create_window(400, 350,window = self.enter_button) #Create a window for the check button

    def authorise_page(self):
        object_list.clear() #Clear the objects list 
        csv_objects('pixel_art_v1.3.csv') #Load the environment for the game using the csv_objects subroutine
        canvas.create_window(80, 250, window = self.picture_entry) #Create a window for the entry box
        canvas.create_window(70, 300,window = self.check_button) #Create a window for the check button
        time.sleep(.2) #Put the program to sleep for 0.2 seconds
        print("loaded")#Print a cue in shell for testing and developer purposes
        Questions.new_question() #Calls the Questions class to retreive and run a new question
        
    #Executes when the left mouse button is clicked
    def left_clicked(self,event):
        for table in object_list: #Cycles through all of the object list
            #Checks against where the mouse was clicked at, finding the corresponding box
            if event.x > table.x1 and event.x < table.x2 and event.y > table.y1 and event.y < table.y2:
                #Checks if the name taken from the box value is one of the following:
                if table.name == "start" :
                    dict['current_page']="authorise" #Change the value of the dict's current_page variable to game
                    self.start() #Runs the start() subroutine.
                if table.name == "exit": self.quit() #Runs the quit subroutine
                #A little hidden easter egg that people might be lucky enough to find.
                if table.name == "easteregg": canvas.create_text(600,100,fill="purple",text="Jess wants coffee",font="Arial 14",anchor="center")

                #Checks the anchor value is not blank
                if table.anchor != '':
                    #Compares the anchor value + 1 against the answer value. If they are the same, it continues to check name
                    if int(table.anchor)+1 == dict['Answer']:
                        if table.name != "":
                                #Run the subroutine to change the colour of the right box corresponding with the answer. 
                                self.colour_action(table.name, table.anchor)
                                #place a block in case of a previous incorrect answer, and change the name to 'done'
                                canvas.create_rectangle(20,340,110,360,fill = YELLOW, outline = YELLOW, width = 5)
                                table.name = "done"
                                #break


    #Executes with the return button is pressed
    def return_pressed(self,event=None):
        print("return pressed") #Print a cue in shell for testing and developer purposes
        #Checks the current page. If it is the start page, change to game page and run the start subroutine
        if dict['current_page']== "start":
            dict['current_page']="authorise"
            self.start()
        elif dict['current_page'] == "authorise":
            self.age_check()
        else:
            #Run the written_option subroutine
            self.written_option()
        
    def colour_action(self,colour,num):
        Objects.changecolour(self,colour,num)#Change the chosen object to white
        dict['counter']+=1 #Increment the counter
        print("Counter: ", dict['counter'])#Print a counter in shell for testing and developer purposes
        Questions.new_question() #Calls the Questions class to retreive and run a new question

        
    #Checks if the entered character is a digit
    def only_numbers(self,char):
        return char.isdigit()
    
    def written_option(self):
        if self.picture_entry.get()!="": #Checks that there is text in the entry box
            entered_num = int(self.picture_entry.get()) #Allocates a variable to hold the entry value 
            print("entered number: ", entered_num)
            if entered_num == dict['Answer']:
                canvas.create_rectangle(20,340,110,360,fill = YELLOW, outline = YELLOW, width = 5)
                #Cycles through all of the object list
                for table in object_list:
                    #Checks to see whether the anchor tag is blank and is not an anchor command (for text)
                    if table.anchor != ''and table.anchor!="center" and table.anchor !="w":
                        #Compares whether the anchor tag value + 1 is the same as the answer currently in the dict
                        if int(table.anchor)+1 == dict['Answer']:
                            time.sleep(.2) #Sleep the program to give it time to check
                            self.picture_entry.delete("0","end") #Clear the entry box value
                            if table.name != "": #Checks whether the table name is not blank
                                self.colour_action(table.name,table.anchor) #Change the colour of the correct answer square by calling colour action subroutine
                                table.name = "done"#Change the name to done to prevent the question from being asked twice.
                                break
                            else:
                                print("Issue at Written Option Point")#Print statement for developer troubleshooting
            else:
                #Create text to display if answer given is wrong.
                canvas.create_text(70,350,fill="red",text="Incorrect.",font="Arial 14",anchor="center")
                

    def age_check(self):
        if self.age_entry.get()!="":#Checks that there is text in the entry box
            age_given = int(self.age_entry.get())#Allocates a variable to hold the entry value
            print("entered age: ", age_given)
            #Checks age is between the minimum and maximum age
            if age_given >=MINIMUM_AGE and age_given <=MAXIMUM_AGE:
                dict['current_page']="game"
                self.authorise_page()
            else:
                self.age_entry.delete("0","end") #Clear the entry box value
                canvas.create_text(400,500,fill="red",text="Are you the right age?",font="Arial 14",anchor="center") # Show error message
                
                
    
class Objects():
    #Initialize values for Objects class
    def __init__(self,obj_type,x1,y1,x2,y2,fill_colour,out_colour,out_width,text,font,anchor,name,number):
        #Assigns a variable to be what is retreived from the csv_object subroutine
        self.obj_type = obj_type
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        self.fill_colour = fill_colour
        self.out_colour = out_colour
        self.text = text
        self.out_width = out_width
        self.font = font
        self.anchor = anchor
        self.name = name
        self.number = number
        
    #Draw an oval on the canvas with specific parameters
    def oval(self,x1,y1,x2,y2,fill_colour,out_colour,out_width):
        canvas.create_oval(x1,y1,x2,y2,fill=fill_colour,outline=out_colour,width=out_width)
        canvas.update()

    #Draw a rectangle on the canvas with specific parameters
    def rectangle(self,x1,y1,x2,y2,fill_colour,out_colour,out_width):
        canvas.create_rectangle(x1,y1,x2,y2,fill=fill_colour,outline=out_colour,width=out_width)
        canvas.update()
   #Write text on the canvas with specific parameters
    def text(self,x1,y1,fill_colour,text,font,anchor):
        canvas.create_text(x1,y1,fill=fill_colour,text=text,font=font,anchor=anchor)
        canvas.update()

    #Save an object to the object list
    def save_object(self,obj_type,x1,y1,x2,y2,fill_colour,out_colour,out_width,text,font,anchor,name,number):
        new_obj = Objects(obj_type,x1,y1,x2,y2,fill_colour,out_colour,out_width,text,font,anchor,name,number)
        object_list.append(new_obj)

   #Change the colour of the object
    def changecolour(self,new_colour,place_num):
        #Cycles through all of the object list
        for table in object_list:
            if table.anchor == place_num: #Checks if the anchor value is same as the place number passed by the parameters
                table.fill_colour = new_colour #Assigns the new fill colour to be the colour passed through the parameters
                table.out_colour = new_colour #Assigns the new outline colour to be the colour passed through by the parameters
                #Checks whether the object type is an oval, and calls the Objects.oval method to draw an oval at that position
                if table.obj_type == "oval" : Objects.oval(self,table.x1,table.y1,table.x2,table.y2,
                                                       table.fill_colour,table.out_colour,table.out_width)
                #Checks whether the object type is a rectangle, and calls the Objects.rectangle method to draw a rectangle at that position
                if table.obj_type == "rectangle" : Objects.rectangle(self,table.x1,table.y1,table.x2,table.y2,
                                                                 table.fill_colour,table.out_colour,table.out_width)
                #Checks whether the object type is text, and calls the Objects.text method to create text at that position
                if table.obj_type == "text" : Objects.text("",table.x1,table.y1,table.fill_colour,table.text,table.font,table.anchor)
                time.sleep(.2)#Sleep the program for .2 seconds
  
    def refreshlist():
        canvas.delete("all")
        #Cycles through all of the object list
        for table in object_list:
            #Checks whether the object type is an oval, and calls the Objects.oval method to draw an oval at that position
            if table.obj_type == "oval" : Objects.oval("",table.x1,table.y1,table.x2,table.y2,
                                                       table.fill_colour,table.out_colour,table.out_width)
            #Checks whether the object type is a rectangle, and calls the Objects.rectangle method to draw a rectangle at that position
            if table.obj_type == "rectangle" : Objects.rectangle("",table.x1,table.y1,table.x2,
                                                                 table.y2,table.fill_colour,table.out_colour,table.out_width)
            #Checks whether the object type is text, and calls the Objects.text method to create text at that position
            if table.obj_type == "text" : Objects.text("",table.x1,table.y1,table.fill_colour,table.text,table.font,table.anchor)


class Questions():
    #Initialize values for Questions class
    def __init__(self,answer,part1ques,part2ques,operator,status):
        self.answer = answer
        self.part1ques = part1ques
        self.part2ques = part2ques
        self.operator = operator
        self.status = status

    #Save the question to the question list
    def save_question(self,answer,part1ques,part2ques,operator,status):
        new_ques = Questions(answer,part1ques,part2ques,operator,status)
        question_list.append(new_ques)

    #Generate the next question
    def new_question():
        #Check that the counter is at the maximum amount of squares
        if dict['counter']== 225:
            time.sleep(3)
            #Create a rectangle to cover an incorrect sign
            canvas.create_rectangle(15,230,150,285,fill = YELLOW, outline = YELLOW, width = 5)
            #Create a rectangle to pop up with Completion message
            canvas.create_rectangle(180,200,620,400,fill = DUSTY_BLUE, outline = DUSTY_BLUE, width = 5)
            canvas.create_text(400,300,fill="gold",text="Congrats! You've completed\nthe Star Colour by Math!",font="Arial 16",anchor="center")
        else:
            #Generate a new random number
            randnum = random.randint(1,225)
            print(randnum)#Print the random number for troubleshooting
            #Cover old question with rectangle
            canvas.create_rectangle(15,170,150,195,fill = YELLOW, outline = YELLOW, width = 5)
            #Check the random number isnt a question that has already been asked
            for table in question_list:
                if randnum == table.answer:
                    if table.status != "done":
                        table.status = "done"
                        #Print the new question
                        ques_text = "{} {} {} = ".format(table.part1ques,table.operator,table.part2ques)
                        canvas.create_text(20,190,fill="black",text=ques_text,font="Arial 16",anchor="w")
                        #Update the canvas with the question
                        canvas.update()
                        #Change the current value of the answer to be for the right square
                        dict['Answer'] = table.answer
                    #Run again if question has already been done
                    elif table.status == "done":
                        Questions.new_question()
                    else:
                        #Troubleshooting message
                        print("Issue creating new question.")
           
                
            
def csv_objects(csv_file):
    print("arrived at csv")
    file = open(csv_file, "r")#Opens the csv file provided
    count = 1 #Starts a counter from 1 (to ignore header row)
    num_lines = sum(1 for line in open(csv_file))#Find the number of lines in the csv
    line = file.readline() #Read the first line from the file (header line)
    while count < num_lines: #Loop while the count variable is less than the number of lines in the csv file
        line = file.readline() #read a line from the file
        line = line.rstrip() #remove any trailing characters from the string
        csv_col = line.split(",") #Split the line read at each ',' it encounters
        #Assign the header labels and initialising them in the Objects class
        if count == 1 : new_obj = Objects(csv_col[0],int(csv_col[1]),int(csv_col[2]),int(csv_col[3]),
                                          int(csv_col[4]),csv_col[5],csv_col[6],csv_col[7],csv_col[8],
                                          csv_col[9],csv_col[10],csv_col[11],int(csv_col[12]))
        #Save the new object to the object list
        new_obj.save_object(csv_col[0],int(csv_col[1]),int(csv_col[2]),int(csv_col[3]),int(csv_col[4]),csv_col[5],csv_col[6],csv_col[7],csv_col[8],csv_col[9],csv_col[10],csv_col[11],int(csv_col[12]))
        count = count + 1 #Increment the counter
    file.close() #Close the file
    Objects.refreshlist() #Clear the canvas and draw the environment from the objects

def csv_questions():
    file = open('maths_questions.csv')#Opens the maths question csv file
    count = 1 #Starts a counter from 1 (to ignore header row)
    num_lines = sum(1 for line in open('maths_questions.csv'))#Find the number of lines in the csv
    line = file.readline()#Read the first line from the file (header line)
    while count < num_lines: #Loop while the count variable is less than the number of lines in the csv file
        line = file.readline() #read a line from the file
        line = line.rstrip() #remove any trailing characters from the string
        csv_col = line.split(",") #Split the line read at each ',' it encounters
        #Assign the header labels and initialising them in the Questions class
        if count == 1 : new_ques = Questions(int(csv_col[0]),int(csv_col[1]),int(csv_col[2]),csv_col[3], csv_col[4])
        #Save the new question to the question list
        new_ques.save_question(int(csv_col[0]),int(csv_col[1]),int(csv_col[2]),csv_col[3],csv_col[4])
        count = count + 1 #Increment the counter
    file.close() #close the file

#Initialise lists and dictionaries
object_list = []
question_list = []
dict = {"Colour":"black", "counter":0,"Answer":0,"current_page":"start"}
#Assign the Tk GUI function to a variable.
main_window = Tk()
main_window.title("Colour By Math") #Give the menu a title
canvas = Canvas(main_window, width=800, height=600, bg=YELLOW) #Initialise the canvas
canvas.grid()

csv_questions()                #Get the questions from the question csv and initialise them in the question list
csv_objects('landing_env.csv') #initialise the landing environment for the front page
window_one()                   #Start the game window


