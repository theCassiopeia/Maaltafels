#Import statements
from tkinter import *

import os
import random
import time

__DEBUG__ = False  #Setting to True generates more print-statementsa
#This parameter can be changed through the preferences menu item since Aug21,2015
aantal_oefeningen = 10

# hoe spelers en hun scores opslaan?
#? dictionary
# profiles = {'naam':"", 'scores':[]}
# ID moet wellicht niet meegenomen worden aangezien Spelers een LIST is
# TO DO : toevoegen tijden waarop de oefening gemaakt is - is deel van de Scores list : bv [score, time]

# Spelers is een list van profielen
Spelers = []
Aantal_gekende_spelers = 0
max_tafels = 10   # geeft de hoogste tafel weer

def toggleDebug():
    global __DEBUG__  #global moeten toevoegen want anders was er een fout dat __DEBUG__ een lokale variabele was die nog niet geinitialiseerd werd
    global aantal_oefeningen
    global debugTk
    
    if debugTk.get():
        __DEBUG__ = True
        aantal_oefeningen = 5 #geeft weer hoeveel oefeningen er komen per reeks
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
    if __DEBUG__:
        print("Reading in data")
    data_file = open('maaltafels.cfg')
    for line in data_file:
        player = eval(line)
        Spelers.append(player)
    data_file.close()
    if __DEBUG__:
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

    def function_generiek(self):
        if __DEBUG__:
            print(self.hOef)

        if self.hOef <= aantal_oefeningen:
            self.factor = int(round(random.random()*10,0)) #lijkt meer random te zijn dan volgende regel
            #factor = randint(0,10)
            if self.rnd:
                self.tafel = int(round(random.random()*10,0))
            self.ans = self.factor * self.tafel

            choice = random.randint(0,1) #when self.mofd == "rnd", this line will choose either "maal" or "deel"
            if self.mofd == "maal" or choice == 0 :
                self.labelFactor.config(text = str(self.factor))
                self.labelTafel.config(text = str(self.tafel))
                self.labelMaal.config(text = "x")
                self.mofdHuidig="maal"
                
            else: # self.mofd == "deel" or choice == 1
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
            self.vraagStr = "Einde!!! \n Je behaalde " + str(self.score) + " punten in " + str(int((self.stoptime - self.starttime)//60)) + " minuten en " +str(int(round((self.stoptime - self.starttime)%60,0))) + " seconden."
            self.labelVraag.config(text=self.vraagStr, fg="green")
            self.inputField.delete(0,END)
            self.inputField.pack_forget()
            self.labelTitel.config(text="", fg="green")
            self.labelFactor.config(text="")
            self.labelTafel.config(text="")
            self.labelMaal.config(text="")
            scoreOef = [self.score, round(self.stoptime - self.starttime,1)]
            Scores_speler.append(scoreOef)
            self.startButton.pack(side=LEFT)
            self.startButton.config(state=NORMAL)

            Score.update(scoreApp)

    def selectTafel(self):
        self.inputField.config(state=NORMAL)
        s = 'Welke tafels wil je oefenen (0 tot {})??? '.format(max_tafels)
        self.labelVraag.config(text=s, fg="green")

    def initOef(self):
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
        self.titelStr = 'Je koos : specifieke maaltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="maal"
        self.rnd=False
        self.selectTafel()
    
    def function_deel(self):
        self.initOef()
        self.titelStr = 'Je koos : specifieke deeltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="deel"
        self.rnd=False
        self.selectTafel()
    
    def function_rnd_maal(self):
        self.initOef()
        self.titelStr = 'Je koos : random maaltafels'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="maal"
        self.rnd=True
        self.vervolgOef()

    def function_rnd_deel(self):
        self.initOef()
        self.titelStr = 'Je koos : random deeltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="deel"
        self.rnd=True
        self.vervolgOef()
    
    def function_rnd_all(self):
        self.initOef()
        self.titelStr = 'Je koos : random maal- en deeltafels'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="rnd"
        self.rnd=True
        self.vervolgOef()

    def selectOefening(self):
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
        
        self.labelSelOef = Label(self.vraagContainer, text="Mogelijke oefeningen", fg="green")
        self.labelSelOef.pack(side=LEFT)
        self.oefA = Button(self.probleemContainer, text="Oefen specifieke maaltafel", command=self.function_maal)
        self.oefA.pack()
        self.oefB = Button(self.probleemContainer, text="Oefen specifieke deeltafel", command=self.function_deel)
        self.oefB.pack()
        self.oefC = Button(self.probleemContainer, text="Oefen random maaltafels", command=self.function_rnd_maal)
        self.oefC.pack()
        self.oefD = Button(self.probleemContainer, text="Oefen random deeltafels", command=self.function_rnd_deel)
        self.oefD.pack()
        self.oefE = Button(self.probleemContainer, text="Oefen random maal- en deeltafels", command=self.function_rnd_all)
        self.oefE.pack()

    def vervolgOef(self):            
        self.hOef = 1        
        self.score = 0
        self.starttime = time.time()
        self.labelVraag.config(text="Hoeveel is", fg="green")
        self.function_generiek()

    def selectSpeler(self):
        self.labelSelSpeler = Label(self.vraagContainer, text="Selecteer een gekende speler of maak een nieuwe speler aan", fg="green")
        self.labelSelSpeler.pack(side=LEFT)
        self.selectedSpeler=StringVar()
        self.selectedSpeler.set("Nieuwe Speler")
        
        for player in Spelers:
            self.b = Radiobutton(self.probleemContainer, text=player['Naam'], variable=self.selectedSpeler, fg="blue")
            self.b.pack()
        self.b = Radiobutton(self.probleemContainer, text="Nieuwe Speler", variable=self.selectedSpeler, fg="red")
        self.b.pack()

        """
    print('selecteer een gekende speler of maak een nieuwe speler aan')
    i  =  0
    for player in Spelers:
        i += 1
        print(i, ' ', player['Naam'])
    i += 1
    print(i, '  Maak een nieuwe speler aan')
    select_speler = input('Maak je keuze : ')
    if not select_speler.isdigit() :
        print('Ongeldige keuze (digits)')
    else:
        select_speler = int(select_speler)
        if (select_speler > Aantal_gekende_spelers + 1) or (select_speler < 1) :
            print('Ongeldige keuze (out of range)')
        elif select_speler == Aantal_gekende_spelers + 1 :
            # creeer nieuwe speler
            Profiel = {'Naam':"", 'Scores':[]}
            print('Je koos om een nieuwe speler te creeeren.')
            Naam_speler = input('Naam : ')
            spelerBestaat = False
            for player in Spelers:
                if Naam_speler == player['Naam']:
                    print('Naam bestaat al')
                    spelerBestaat = True
                    break
            if spelerBestaat == False:
                # m.a.w. geen enkele "player" heeft een 'naam' gelijk aan Naamspeler, d.w.z. dat er geen break is geweest in de For loop
                #dan moeten we uit de True-while loop en doorgaan met aanmaken van nieuwe gebruiker
                Profiel['Naam'] = Naam_speler
                Scores_speler = []
                Profiel['Scores'] = Scores_speler
                Aantal_gekende_spelers += 1
                Spelers.append(Profiel)
                write_config(Spelers) 
                break

        else:
            Naam_speler = Spelers[select_speler-1]['Naam']
            Scores_speler = Spelers[select_speler-1]['Scores']
            break
     # Voeg nieuwe speler toe aan de configuratie file
"""
        
    def __init__(self, myParent):
        self.myParent = myParent
        self.titelContainer = Frame(myParent)
        self.titelContainer.pack()
        self.vraagContainer = Frame(myParent)
        self.vraagContainer.pack()
        self.labelVraag = Label(self.vraagContainer, text="", fg="green")
        self.labelVraag.pack(side=LEFT)
        self.probleemContainer = Frame(myParent)
        self.probleemContainer.pack()
        self.oplossingContainer = Frame(myParent)
        self.oplossingContainer.pack()
        self.mededelingContainer = Frame(myParent)
        self.mededelingContainer.pack()
        self.stopContainer = Frame(myParent)
        self.stopContainer.pack()
        self.startButton = Button(self.stopContainer, text="AGAIN", command=self.selectOefening)
        #self.startButton.pack(side=LEFT)
        #removed these lines since I added a Quit menu item on top of the screen
        #self.stopButton = Button(self.stopContainer, text="STOP", fg="red", command=self.myParent.destroy)
        #self.stopButton.pack(side=LEFT)
        self.labelTitel = Label(self.titelContainer, text="", fg="green")
        self.labelFactor = Label(self.probleemContainer, text = "", font = ("Helvetica", 32))
        self.labelTafel = Label(self.probleemContainer, text = "", font = ("Helvetica", 32))
        self.labelMaal = Label(self.probleemContainer, text = "", font = ("Helvetica", 32))
        self.labelTitel.pack()
        self.labelFactor.pack(side=LEFT)
        self.labelMaal.pack(side=LEFT)
        self.labelTafel.pack(side=LEFT)
        self.inputField = Entry(self.oplossingContainer, font = ("Helvetica", 16), justify=CENTER, width=5)
        self.inputField.bind("<Return>", self.evaluate)
        #self.inputField.pack()
        #commented out since the startOef function performs the pack.
        #A pack_forget is performed at the end of a sequence to clean up the screen
        self.labelMededeling = Label(self.mededelingContainer, text="", fg="green")
        self.labelMededeling.pack()        
        self.startButton.focus()

        #self.selectOefening()
        self.selectSpeler()
    

class Score(Frame):
    def __init__(self, myParent):
        self.myParentScore = myParent
        self.scoreContainer = Frame(myParent)
        self.scoreContainer.pack()
        s='Naam      Score    Tijd\n'
        for player in Spelers:
            for score in player['Scores']:
                s += "{0:<10s}{1:5d}{2:8.2f}\n".format(player['Naam'],score[0],score[1])
        if __DEBUG__:
            print(s)
        self.scoreList = Text(self.scoreContainer)
        self.scoreList.pack()
        self.scoreList.insert(END, s)

    def update(self):
        s='Naam      Score    Tijd\n'
        for player in Spelers:
            for score in player['Scores']:
                s += "{0:<10s}{1:5d}{2:8.2f}\n".format(player['Naam'],score[0],score[1])
        if __DEBUG__:
            print(s)
        self.scoreList.replace(1.0, END, s)

# Lees Config file
if os.path.isfile('maaltafels.cfg'):
    read_config()
    Aantal_gekende_spelers = len(Spelers)

s='aantal gekende spelers = {}'.format(Aantal_gekende_spelers)
if __DEBUG__:
    print(s)
    
# parse through lines
# Selecteer speler of creeer een nieuwe speler
""""
while True:
    print('selecteer een gekende speler of maak een nieuwe speler aan')
    i  =  0
    for player in Spelers:
        i += 1
        print(i, ' ', player['Naam'])
    i += 1
    print(i, '  Maak een nieuwe speler aan')
    select_speler = input('Maak je keuze : ')
    if not select_speler.isdigit() :
        print('Ongeldige keuze (digits)')
    else:
        select_speler = int(select_speler)
        if (select_speler > Aantal_gekende_spelers + 1) or (select_speler < 1) :
            print('Ongeldige keuze (out of range)')
        elif select_speler == Aantal_gekende_spelers + 1 :
            # creeer nieuwe speler
            Profiel = {'Naam':"", 'Scores':[]}
            print('Je koos om een nieuwe speler te creeeren.')
            Naam_speler = input('Naam : ')
            spelerBestaat = False
            for player in Spelers:
                if Naam_speler == player['Naam']:
                    print('Naam bestaat al')
                    spelerBestaat = True
                    break
            if spelerBestaat == False:
                # m.a.w. geen enkele "player" heeft een 'naam' gelijk aan Naamspeler, d.w.z. dat er geen break is geweest in de For loop
                #dan moeten we uit de True-while loop en doorgaan met aanmaken van nieuwe gebruiker
                Profiel['Naam'] = Naam_speler
                Scores_speler = []
                Profiel['Scores'] = Scores_speler
                Aantal_gekende_spelers += 1
                Spelers.append(Profiel)
                write_config(Spelers) 
                break

        else:
            Naam_speler = Spelers[select_speler-1]['Naam']
            Scores_speler = Spelers[select_speler-1]['Scores']
            break
     # Voeg nieuwe speler toe aan de configuratie file


s='Naam van geselecteerde speler = {}'.format(Naam_speler)
print(s)
s='Scores van geselecteerde speler = {}'.format(Scores_speler)
print(s)
"""

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
root.config(menu=menubar)
root.attributes("-topmost", True) #om te zorgen dat het window op de voorgrond komt te staan

scoreWindow = Toplevel()
scoreWindow.geometry("300x500+420+100")
scoreWindow.attributes("-topmost", True)
scoreWindow.title("HIGH-SCORES")

app = Application(root)

scoreApp = Score(scoreWindow)

root.mainloop()

write_config(Spelers)

# Limit number of scores to 10

