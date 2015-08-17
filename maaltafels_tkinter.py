#Import statements
from tkinter import *

import os
import random
import time

__DEBUG__ = True  #Setting to True generates more print-statements

# selecteer speler of creeer een nieuwe speler

# selecteer opgave
# - maaltafels (0 - 10)
# - deeltafels (0 - 10)
# - random maaltafels
# - random deeltafels
# - random maal- of deeltafels

# hoe spelers en hun scores opslaan?
#? dictionary
# profiles = {'naam':"", 'scores':[]}
# ID moet wellicht niet meegenomen worden aangezien Spelers een LIST is
# TO DO : toevoegen tijden waarop de oefening gemaakt is - is deel van de Scores list : bv [score, time]

# Spelers is een list van profielen
Spelers = []
Aantal_gekende_spelers = 0
max_tafels = 10   # geeft de hoogste tafel weer
if __DEBUG__:
    aantal_oefeningen = 5 #geeft weer hoeveel oefeningen er komen per reeks
else:
    aantal_oefeningen = 10

def toggleDebug():
    global __DEBUG__   #global moeten toevoegen want anders was er een fout dat __DEBUG__ een lokale variabele was die nog niet geinitialiseerd werd
    global debugTk
    print(__DEBUG__, debugTk)
    #__DEBUG__ = not(__DEBUG__)
    #if __DEBUG__:
    #    aantal_oefeningen = 5 #geeft weer hoeveel oefeningen er komen per reeks
    #    print(__DEBUG__)
    #else:
    #    aantal_oefeningen = 10    

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
#insert all code for selecting a maaltafel and do the test
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
                        #print("Correct")
                        self.score += 1
                    else:
                        self.mededelingStr = "Fout. Het moest " + str(self.ans) + " zijn!!! "
                        self.labelMededeling.config(text=self.mededelingStr, fg="red")
                        #print("Fout. Het moest" + self.ans + " zijn!!! " )
                else: #self.mofdHuidg = "deel"
                    if int(inp) == self.factor:
                        self.mededelingStr = "Correct"
                        self.labelMededeling.config(text=self.mededelingStr, fg="green")
                        #print("Correct")
                        self.score += 1
                    else:
                        self.mededelingStr = "Fout. Het moest " + str(self.factor) + " zijn!!! "
                        self.labelMededeling.config(text=self.mededelingStr, fg="red")
                        #print("Fout. Het moest" + self.factor + " zijn!!! " )
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

            if self.mofd == "maal":
                #s = 'Hoeveel is ' + str(factor) + ' x ' + str(self.tafel) + '? '
                self.labelFactor.config(text = str(self.factor))
                self.labelTafel.config(text = str(self.tafel))
                self.labelMaal.config(text = "x")
                self.mofdHuidig="maal"
                
            elif self.mofd == "deel":
                if self.tafel == 0:
                    self.tafel = 1  #om delingen door 0 te vermijden!
                #s = 'Hoeveel is ' + str(ans) + ' / ' + str(tafel) + '? '
                self.labelFactor.config(text = str(self.ans))
                self.labelTafel.config(text = str(self.tafel))
                self.labelMaal.config(text = ":")
                self.mofdHuidig="deel"

            else:    #self.mod = "rnd"
                choice = random.randint(0,1)
                if choice == 0:
                    #s = 'Hoeveel is ' + str(factor) + ' x ' + str(tafel) + '? '
                    self.labelFactor.config(text = str(self.factor))
                    self.labelTafel.config(text = str(self.tafel))
                    self.labelMaal.config(text = "x")
                    self.mofdHuidig="maal"
                else:
                    if self.tafel == 0:
                        self.tafel = 1  #om delingen door 0 te vermijden!
                    #s = 'Hoeveel is ' + str(ans) + ' / ' + str(tafel) + '? '
                    self.labelFactor.config(text = str(self.ans))
                    self.labelTafel.config(text = str(self.tafel))
                    self.labelMaal.config(text = ":")
                    self.mofdHuidig="deel"
            self.inputField.focus()
            #hier komt code voor random maal/deel en random tafel
    
        else:
            self.stoptime = time.time()
            self.vraagStr = "Einde!!! \n Je behaalde " + str(self.score) + " punten in " + str(int((self.stoptime - self.starttime)//60)) + " minuten en " +str(round((self.stoptime - self.starttime)%60,1)) + " seconden."
            self.labelVraag.config(text=self.vraagStr, fg="green")
            self.inputField.delete(0,END)
            self.inputField.pack_forget()
            self.labelTitel.config(text="", fg="green")
            self.labelFactor.config(text="")
            self.labelTafel.config(text="")
            self.labelMaal.config(text="")
            scoreOef = [self.score, round(self.stoptime - self.starttime,1)]
            Scores_speler.append(scoreOef)
            self.startButton.config(state=NORMAL)

            Score.update(scoreApp)

    def function_maal(self):
        #print('Je koos : a - specifieke maaltafel')
        self.titelStr = 'Je koos : a - specifieke maaltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="maal"
        self.rnd=False
        self.function_generiek()
    
    def function_deel(self):
        #print('Je koos : b - specifieke deeltafel')
        self.titelStr = 'Je koos : b - specifieke deeltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="deel"
        self.rnd=False
        self.function_generiek()
    
    def function_rnd_maal(self):
        #print('Je koos : c - random maaltafels')
        self.titelStr = 'Je koos : c - random maaltafels'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="maal"
        self.rnd=True
        self.function_generiek()

    def function_rnd_deel(self):
        #print('Je koos : d - random deeltafel')
        self.titelStr = 'Je koos : d - random deeltafel'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="deel"
        self.rnd=True
        self.function_generiek()
    
    def function_rnd_all(self):
        #print('Je koos : e - random maal- en deeltafels')
        self.titelStr = 'Je koos : e - random maal- en deeltafels'
        self.labelTitel.config(text=self.titelStr, fg="green")
        self.mofd="rnd"
        self.rnd=True
        self.function_generiek()
        
    def __init__(self, myParent, oef):
        self.myParent = myParent
        self.selOef = oef
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
        self.startButton = Button(self.stopContainer, text="START", command=self.startOef)
        self.startButton.pack(side=LEFT)
        self.stopButton = Button(self.stopContainer, text="STOP", fg="red", command=self.myParent.destroy)
        self.stopButton.pack(side=LEFT)
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
    
    
    def startOef(self):
        self.hOef = 0
        self.inputField.pack()
        self.inputField.focus()
        self.startButton.config(state=DISABLED)
        self.inputField.config(state=NORMAL)
        if self.selOef in ['a', 'b']:
            s = 'Welke tafels wil je oefenen (0 tot {})??? '.format(max_tafels)
            self.labelTitel.config(text=s, fg="green")
        else:
            self.vervolgOef()
                
    def vervolgOef(self):            
        functions = {'a': self.function_maal,
                     'b': self.function_deel,
                     'c': self.function_rnd_maal,
                     'd': self.function_rnd_deel,
                     'e': self.function_rnd_all}
        self.func = functions[self.selOef]
        self.hOef = 1        
        self.score = 0
        self.starttime = time.time()
        self.labelVraag.config(text="Hoeveel is", fg="green")
        self.func()

class Score(Frame):
    def __init__(self, myParent):
        self.myParentScore = myParent
        self.scoreContainer = Frame(myParent)
        self.scoreContainer.pack()
        s='Naam      Score    Tijd\n'
        for player in Spelers:
            for score in player['Scores']:
                s += "{0:<10s}{1:5d}{2:8.2f}\n".format(player['Naam'],score[0],score[1])
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
print(s)
    
# parse through lines
# Selecteer speler of creeer een nieuwe speler
# TO DO : selecteer speler
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
    # TO DO : check of de naam al voorkomt in de bestaande profielen
    
     # Voeg nieuwe speler toe aan de configuratie file


s='Naam van geselecteerde speler = {}'.format(Naam_speler)
print(s)
s='Scores van geselecteerde speler = {}'.format(Scores_speler)
print(s)

# selecteer opgave
# - maaltafels (0 - 10)
# - deeltafels (0 - 10)
# - random maaltafels
# - random deeltafels
# - random maal- of deeltafels
print('Mogelijke oefeningen')
print('a - Oefen specifieke maaltafel')
print('b - Oefen specifieke deeltafel')
print('c - Oefen random maaltafels')
print('d - Oefen random deeltafels')
print('e - Oefen random maal- en deeltafels')

while True:
    select_oefening = input('Maak je keuze: ')
    if select_oefening in ['a', 'b', 'c', 'd', 'e']:
        break
    else:
        print('Foute ingave!!')

root = Tk()


menubar = Menu(root)
debugTk = BooleanVar()
menubar.add_checkbutton(label="Debug", onvalue=True, offvalue=False, variable=debugTk, command=toggleDebug)
menubar.add_command(label="Quit!", command=root.destroy)
root.title("Maaltafels oefenen ...")
root.geometry("300x200+100+100")
root.config(menu=menubar)
root.attributes("-topmost", True) #om te zorgen dat het window op de voorgrond komt te staan

scoreWindow = Toplevel()
scoreWindow.geometry("300x500+420+100")
scoreWindow.attributes("-topmost", True)
scoreWindow.title("HIGH-SCORES")

app = Application(root, select_oefening)

scoreApp = Score(scoreWindow)

root.mainloop()

write_config(Spelers)

# Show High-Scores

# Limit number of scores to 10

