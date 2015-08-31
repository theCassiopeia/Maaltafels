#Import statements
from tkinter import *

import os
import random
import time

# profiles = {'naam':"", 'scores':[]}
# TO DO : toevoegen tijden waarop de oefening gemaakt is - is deel van de Scores list : bv [score, time]

# Spelers is een list van profielen

#Global variables
__DEBUG__ = False  #Setting to True generates more print-statements - This parameter can be changed through the preferences menu item since Aug21,2015
aantal_oefeningen = 10 #geeft weer hoeveel oefeningen er komen per reeks
max_tafels = 10   # geeft de hoogste tafel weer
Spelers = []
Naam_speler = ""
Scores_speler = []
Aantal_gekende_spelers = 0

def toggleDebug():
    global __DEBUG__
    #global moeten toevoegen want anders was er een fout dat __DEBUG__ een lokale variabele was die nog niet geinitialiseerd werd
    #is enkel nodig indien er een assignment is aan de variabele !
    global aantal_oefeningen
    
    if debugTk.get(): #geen globale variable, want er komt geen assignment aan debugTk, enkel uitlezen
        __DEBUG__ = True
        aantal_oefeningen = 5 
        print("TRUE")
    else:
        __DEBUG__ = False
        aantal_oefeningen = 10
        print("FALSE")

def write_config(players):
    if __DEBUG__:
        print("Saving maaltafel profielen")
    data_file = open('maaltafels.cfg', 'w')
    lines = []
    for player in Spelers:
        lines.append(repr(player) + '\n')
    data_file.writelines(lines)
    data_file.close
    return

def read_config():
    global Aantal_gekende_spelers
    # Lees Config file
    if os.path.isfile('maaltafels.cfg'):
        if __DEBUG__:
            print("Reading in data")
        data_file = open('maaltafels.cfg')
        for line in data_file:
            player = eval(line)
            Spelers.append(player)
        data_file.close()
        Aantal_gekende_spelers = len(Spelers)
        if __DEBUG__:
            s='aantal gekende spelers = {}'.format(Aantal_gekende_spelers)
            print(s)
            print(Spelers)
    return    

class Application(Frame):
    def evaluate(self, event):
        inp = self.inputField.get()
        self.labelMededeling.config(text="", fg="red")
        if inp.isdigit():              
            if self.hOef == 0:
                self.tafel = int(inp)
                if self.tafel not in list(range(0, max_tafels+1)):
                    self.labelTitel.config(text="Deze tafels kun je niet oefenen...", fg="red")
                    time.sleep(3)
                    s = 'Welke tafels wil je oefenen (0 tot {})??? '.format(max_tafels)
                    self.labelTitel.config(text=s, fg="green")
                    self.inputField.delete(0,END)
                else:
                    self.inputField.delete(0,END)
                    self.vervolgOef()

            else:
                if self.mofdHuidig=="maal":
                    if int(inp) == self.ans:
                        self.mededelingStr = "Correct"
                        self.labelMededeling.config(text=self.mededelingStr, fg="green")
                        self.score += 1
                    else:
                        self.mededelingStr = "Fout. Het moest " + str(self.ans) + " zijn!!! "
                        self.labelMededeling.config(text=self.mededelingStr, fg="red")
                else: #self.mofdHuidg = "deel"
                    if int(inp) == self.factor:
                        self.mededelingStr = "Correct"
                        self.labelMededeling.config(text=self.mededelingStr, fg="green")
                        self.score += 1
                    else:
                        self.mededelingStr = "Fout. Het moest " + str(self.factor) + " zijn!!! "
                        self.labelMededeling.config(text=self.mededelingStr, fg="red")
                self.hOef += 1
                self.inputField.delete(0,END)
                self.function_generiek()
        else:
            self.mededelingStr = "Foute ingave"
            self.labelMededeling.config(text=self.mededelingStr, fg="red")
            #time.sleep(3) --- combinatie van sleep en veranderen van labels schijnt niet goed te werken !!!
            #self.labelMededeling.config(text="", fg="red")
            self.inputField.delete(0,END)

    def evaluateSpeler(self, event):
        global Aantal_gekende_spelers
        global Naam_speler
        global Scores_speler
        
        self.labelSelSpeler.pack_forget()
        Naam_speler = self.inputField.get()
        self.inputField.delete(0,END)
        self.inputField.pack_forget()
        
        spelerBestaat = False
        for player in Spelers:
            if Naam_speler == player['Naam']:
                self.labelVraag.config(text="De ingegeven naam bestaat al !!", fg="red")
                spelerBestaat = True
                break
            
        if spelerBestaat:
            self.selectSpeler() #opnieuw speler selecteren
        else:
            # m.a.w. geen enkele "player" heeft een 'naam' gelijk aan Naam_speler, d.w.z. dat er geen break is geweest in de For loop
            #dan moeten we uit de True-while loop en doorgaan met aanmaken van nieuwe gebruiker
            Profiel = {'Naam':"", 'Scores':[]}
            Profiel['Naam'] = Naam_speler
            Scores_speler = []
            Profiel['Scores'] = Scores_speler
            Aantal_gekende_spelers += 1
            Spelers.append(Profiel)
            if __DEBUG__:
                print(Spelers)
            write_config(Spelers)
            
            self.selectOefening()

    def function_generiek(self):
        global Naam_speler
        global Scores_speler

        if __DEBUG__:
            print(self.hOef)

        if self.hOef <= aantal_oefeningen:
            self.factor = int(round(random.random()*10,0)) #lijkt meer random te zijn dan volgende regel
            #factor = randint(0,10)
            if self.rnd:
                self.tafel = int(round(random.random()*10,0))
            self.ans = self.factor * self.tafel

            choice = random.randint(0,1) #when self.mofd == "rnd", this line will choose either "maal" or "deel"
            if self.mofd == "maal" or (self.mofd == "rnd" and choice == 0) :
                self.labelFactor.config(text = str(self.factor))
                self.labelTafel.config(text = str(self.tafel))
                self.labelMaal.config(text = "x")
                self.mofdHuidig="maal"
                
            else: # self.mofd == "deel" or (self.mofd="rnd" and choice == 1)
                if self.tafel == 0:
                    self.tafel = 1  #om delingen door 0 te vermijden!
                    self.ans = self.factor * self.tafel
                self.labelFactor.config(text = str(self.ans))
                self.labelTafel.config(text = str(self.tafel))
                self.labelMaal.config(text = ":")
                self.mofdHuidig="deel"
                
            self.inputField.focus()

        else:
            self.stoptime = time.time()
            self.scorePercent = int(round(self.score*100/(self.hOef-1),0))
            self.vraagStr = "Einde!!! \n Je behaalde " + "{0:4d}".format(self.scorePercent) + "% in " + str(int((self.stoptime - self.starttime)//60)) + " minuten en " +str(int(round((self.stoptime - self.starttime)%60,0))) + " seconden."
            self.labelVraag.config(text=self.vraagStr, fg="green")
            self.inputField.delete(0,END)
            self.inputField.pack_forget()
            self.labelTitel.config(text="", fg="green")
            self.labelFactor.config(text="")
            self.labelTafel.config(text="")
            self.labelMaal.config(text="")
            scoreOef = [self.scorePercent, round(self.stoptime - self.starttime,1)]
            Scores_speler.append(scoreOef)
            self.startButton.config(text="OPNIEUW", fg="blue", command=self.selectOefening)
            self.startButton.bind("<Return>", self.selectOefening)
            self.startButton.pack(side=LEFT)
            self.startButton.focus()
            self.startButton.config(state=NORMAL)

            Score.update(scoreApp)

    def selectTafel(self):
        self.inputField.config(state=NORMAL)
        s = 'Welke tafels wil je oefenen (0 tot {})??? '.format(max_tafels)
        self.labelVraag.config(text=s, fg="green")

    def initOef(self):
        self.inputField.bind("<Return>", self.evaluate)
        self.inputField.pack()
        self.inputField.focus()
        self.labelSelOef.pack_forget()
        self.oefA.pack_forget()
        self.oefB.pack_forget()
        self.oefC.pack_forget()
        self.oefD.pack_forget()
        self.oefE.pack_forget()
        
    def function_maal(self):
        self.initOef()
        self.titelStr = 'Je koos : bepaalde maaltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="maal"
        self.rnd=False
        self.selectTafel()
    
    def function_deel(self):
        self.initOef()
        self.titelStr = 'Je koos : bepaalde deeltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="deel"
        self.rnd=False
        self.selectTafel()
    
    def function_rnd_maal(self):
        self.initOef()
        self.titelStr = 'Je koos : willekeurige maaltafels'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="maal"
        self.rnd=True
        self.vervolgOef()

    def function_rnd_deel(self):
        self.initOef()
        self.titelStr = 'Je koos : willekeurige deeltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="deel"
        self.rnd=True
        self.vervolgOef()
    
    def function_rnd_all(self):
        self.initOef()
        self.titelStr = 'Je koos : willekeurige maal- en deeltafels'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="rnd"
        self.rnd=True
        self.vervolgOef()

    def selectOefening(self, event=None):
        #event=None added => Again knop has now bound to pressing <Return> as well,
        #                    but generates two parameters to the function
        # selecteer opgave
        # - maaltafels (0 - 10)
        # - deeltafels (0 - 10)
        # - random maaltafels
        # - random deeltafels
        # - random maal- of deeltafels
        self.hOef = 0
        self.startButton.pack_forget()
        self.labelVraag.config(text="", fg="green")
        self.labelMededeling.config(text="", fg="green")
        
        self.labelSelOef = Label(self.vraagContainer, text="Mogelijke oefeningen", fg="green", bg="white")
        self.labelSelOef.pack(side=LEFT)
        self.oefA = Button(self.probleemContainer, text="Oefen bepaalde maaltafel", command=self.function_maal, width=30)
        self.oefA.pack()
        self.oefB = Button(self.probleemContainer, text="Oefen bepaalde deeltafel", command=self.function_deel, width=30)
        self.oefB.pack()
        self.oefC = Button(self.probleemContainer, text="Oefen willekeurige maaltafels", command=self.function_rnd_maal, width=30)
        self.oefC.pack()
        self.oefD = Button(self.probleemContainer, text="Oefen willekeurige deeltafels", command=self.function_rnd_deel, width=30)
        self.oefD.pack()
        self.oefE = Button(self.probleemContainer, text="Oefen willekeurige maal- en deeltafels", command=self.function_rnd_all, width=30)
        self.oefE.pack()

    def vervolgOef(self):            
        self.hOef = 1        
        self.score = 0
        self.starttime = time.time()
        self.labelVraag.config(text="Hoeveel is", fg="green")
        self.function_generiek()

    def selectSpeler(self):
        self.labelSelSpeler = Label(self.vraagContainer,
                                    text="Selecteer een gekende speler \nof maak een nieuwe speler aan",
                                    fg="green", bg="white")
        self.labelSelSpeler.pack()
        self.selectedSpeler=StringVar()
        self.selectedSpeler.set("Nieuwe Speler")
        self.radiobuttons = []
        for player in Spelers:
            b = Radiobutton(self.probleemContainer, text=player['Naam'], variable=self.selectedSpeler,
                            value=player['Naam'], fg="blue", selectcolor="yellow", indicatoron=0, width=15)
            b.pack(anchor=W)
            self.radiobuttons.append(b)
        b = Radiobutton(self.probleemContainer, text="Nieuwe Speler", variable=self.selectedSpeler,
                        value="Nieuwe Speler", fg="red", selectcolor="yellow", indicatoron=0, width=15)
        b.pack(anchor=W)
        self.radiobuttons.append(b)
        self.startButton.config(text="SELECT")
        self.startButton.pack()

    def spelerSelected(self):
        global Naam_speler
        global Scores_speler

        for buttons in self.radiobuttons:
            buttons.pack_forget()
        self.startButton.pack_forget()

        selPlayer = self.selectedSpeler.get()
        self.labelVraag.config(text="") #in case a name was given for a new player which already existed, the text should be deleted.

        if selPlayer == "Nieuwe Speler" :
            self.labelSelSpeler.config(text="Je koos om een nieuwe speler te creeeren.\nGeef een naam:")
            self.inputField.bind("<Return>", self.evaluateSpeler)
            self.inputField.pack()
            self.inputField.focus()

        else:
            self.labelSelSpeler.pack_forget()
            Naam_speler = selPlayer
            for player in Spelers:
                if player['Naam'] == Naam_speler:
                    Scores_speler = player['Scores']
                    break
            if __DEBUG__:
                print(Naam_speler, Scores_speler)

            self.selectOefening()
        
    def __init__(self, myParent):
        self.myParent = myParent
        self.titelContainer = Frame(myParent, bg="white")
        self.titelContainer.pack()
        self.vraagContainer = Frame(myParent, bg="white")
        self.vraagContainer.pack()
        self.labelVraag = Label(self.vraagContainer, text="", fg="green", bg="white")
        self.labelVraag.pack()
        self.probleemContainer = Frame(myParent, bg="white")
        self.probleemContainer.pack()
        self.oplossingContainer = Frame(myParent, bg="white")
        self.oplossingContainer.pack()
        self.mededelingContainer = Frame(myParent, bg="white")
        self.mededelingContainer.pack()
        self.stopContainer = Frame(myParent, bg="white")
        self.stopContainer.pack()
        self.startButton = Button(self.stopContainer, text="", command=self.spelerSelected)
        self.labelTitel = Label(self.titelContainer, text="", fg="green", bg="white")
        self.labelFactor = Label(self.probleemContainer, text = "", font = ("Helvetica", 32), bg="white")
        self.labelTafel = Label(self.probleemContainer, text = "", font = ("Helvetica", 32), bg="white")
        self.labelMaal = Label(self.probleemContainer, text = "", font = ("Helvetica", 32), bg="white")
        self.labelTitel.pack()
        self.labelFactor.pack(side=LEFT)
        self.labelMaal.pack(side=LEFT)
        self.labelTafel.pack(side=LEFT)
        self.inputField = Entry(self.oplossingContainer, font = ("Helvetica", 16), justify=CENTER,
                                width=15, bg="yellow")
        
        #self.inputField.pack()
        #commented out since the startOef function performs the pack.
        #A pack_forget is performed at the end of a sequence to clean up the screen
        self.labelMededeling = Label(self.mededelingContainer, text="", fg="green", bg="white")
        self.labelMededeling.pack()        
        self.startButton.focus()

        #self.selectOefening()
        self.selectSpeler()
    

class Score(Frame):
    def __init__(self, myParent):
        self.myParentScore = myParent
        self.scoreContainer = Frame(myParent, bg="white")
        self.scoreContainer.pack()
        s='Naam      Score      Tijd\n'
        for player in Spelers:
            for score in player['Scores']:
                tijdStr = "{0:6.0f}".format(int(score[1]//60)) + "'" + "{0:2.0f}".format(int(round(score[1]%60,0))) + "\""
                s += "{0:<10s}{1:4d}%".format(player['Naam'],int(score[0])) + tijdStr+ "\n"
        if __DEBUG__:
            print(s)
        self.scoreList = Text(self.scoreContainer)
        self.scoreList.pack()
        self.scoreList.insert(END, s)

    def update(self):
        s='Naam      Score      Tijd\n'
        for player in Spelers:
            for score in player['Scores']:
                tijdStr = "{0:6.0f}".format(int(score[1]//60)) + "'" + "{0:2.0f}".format(int(round(score[1]%60,0))) + "\""
                s += "{0:<10s}{1:4d}%".format(player['Naam'],int(score[0])) + tijdStr+ "\n"
        if __DEBUG__:
            print(s)
        self.scoreList.replace(1.0, END, s)


    
# parse through lines
# Selecteer speler of creeer een nieuwe speler

read_config()

root = Tk()

debugTk = BooleanVar()
debugTk.set(False)

menubar = Menu(root)
prefMenu = Menu(menubar, tearoff=0)

prefMenu.add_checkbutton(label="Debug", onvalue=True, offvalue=False, variable=debugTk, command=toggleDebug)
menubar.add_cascade(label="Preferences", menu=prefMenu)
menubar.add_command(label="Quit!", command=root.destroy)
root.title("Maaltafels oefenen ...")
root.geometry("300x250+100+100")
root.config(menu=menubar, bg="white")
root.attributes("-topmost", True) #om te zorgen dat het window op de voorgrond komt te staan

scoreWindow = Toplevel()
scoreWindow.geometry("300x500+420+100")
scoreWindow.attributes("-topmost", True)
scoreWindow.title("HIGH-SCORES")
scoreWindow.config(bg="white")

app = Application(root)

scoreApp = Score(scoreWindow)

root.mainloop()

write_config(Spelers)

# Limit number of scores to 10

