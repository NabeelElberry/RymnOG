import math
import threading
import tkinter as tk
from datetime import date
from datetime import datetime
from datetime import timedelta
import re
import pickle
import schedule
import time
from threading import Timer
from tkinter import *
from plyer import notification
from pystray import MenuItem as itemzzz
import pystray
import PIL.Image
import PIL.ImageTk
import random
from tkinter import ttk
import pyglet
import sv_ttk
import os
import shutil
import textwrap

# Nabeel Elberry
# Rymn Program v1.0
# Started 6/11/23

class Item: 
    item_name = ""
    item_definition = ""
    item_level = "0"
    date_to_review = "" # string
    hour_to_review = 0 # int
    gotten_wrong = False
    previous_item_lvl = 0 # int
    alternate_definitions = []
    def __init__(self, item_name, item_definition, alt_defn):
        self.item_name = item_name
        self.item_definition = item_definition
        self.item_level = "0"
        self.date_to_review = "" # string
        self.hour_to_review = 0 # int
        self.gotten_wrong = False
        self.previous_item_lvl = 0
        self.alternate_definitions = alt_defn
    def __lt__(self, otherItem):
        return self.item_name < self.otherItem.item_name
    def __gt__(self, otherItem):
        return self.item_name > self.otherItem.item_name
    def __le__(self, otherItem):
        return self.item_name <= self.otherItem.item_name
    def __ge__(self, otherItem):
        return self.item_name >= self.otherItem.item_name
    def __ne__(self, otherItem):
        return self.item_name != self.otherItem.item_name
    def __eg__(self, otherItem):
        return self.item_name == self.otherItem.item_name
    def __repr__(self) -> str:
        return f"\nterm: {self.item_name}, defn: {self.item_definition}, dateReview: {self.date_to_review}, hourToReview: {self.hour_to_review}, level: {self.item_level}, alternate defns: {self.alternate_definitions}"
    def updateHoursAndTime(self, newDate, newHour):
        self.date_to_review = newDate
        self.hour_to_review = newHour
# imported tooltip
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#1c1c1c", relief=SOLID, borderwidth=1,
                      font=("Louis George Cafe", "10", "normal"), fg = '#e3e3e3')
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

################################ Start of my code


deleteItem = None
itemFinder = {"0": [], 
                        "1": [],
                        "2": [],
                        "3": [],
                        "4": [],
                        "5": [],
                        "6": [],
                        "7": []
                        }
dailyLoadUp = {
        "0": [],
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        "9": [],
        "10": [],
        "11": [],
        "12": [],
        "13": [],
        "14": [],
        "15": [],
        "16": [],
        "17": [],
        "18": [],
        "19": [],
        "20": [],
        "21": [],
        "22": [],
        "23": []
    }
currReviewList = []
previousDirect = None
notes = set()
currDir = None
termLimit = (datetime.date, 30)

class MainGUI:
    def __init__(self):
        self.t_entry = None
        self.d_entry = None
        self.curr_frame = None      
        self.addToDailyLoadUp()
        self.checkReviewsOnStartup()
        #GUI Start
        self.root = tk.Tk()
        self.root.iconbitmap("rymn.ico")
        self.term_entry = tk.StringVar()
        self.defn_entry = tk.StringVar()
        pyglet.font.add_file("cafe.ttf")
        self.root.geometry("900x900")
        self.root.title("Rymn")
        self.root.tk.call('source', 'forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')
        
        # choose which profile:
        filepath = './profiles'
        subdirectories = os.walk(filepath)
        self.btn_frame = tk.Frame(self.root)
        count = 0
        iY = 1
        iX = 1
        # usedItem = None
    
        btn = tk.Button(self.btn_frame, text = "Add Profile", font = ('Louis George Cafe', 20), command = lambda: self.showFrame('addLang'))
        btn.grid(row = iX, column = 0)

        for item in subdirectories:
            for name in item[1]:
                count +=1
                if item != []:
                    if iY == 4:
                        iY = 0
                        iX +=1
                    button = tk.Button(self.btn_frame, text = f"{name}", font = ('Louis George Cafe', 20), command = lambda m = name: self.whichToUse(m))
                    button.grid(row = iX, column = iY, padx = (5, 0))
                    iY+=1
        #profile_frame = tk.Frame(self.root)
        profile_prompt = tk.Label(self.btn_frame, text = "Which profile do you want to use?", font = ('Louis George Cafe', 18))
        profile_prompt.grid(row = 0, column = 0, columnspan= count+1, pady = (0, 5))
        self.btn_frame.pack()
        
            
            

        # Menu stuff
        self.framesHold = [None, None, None, 
                           None, None, None, 
                           None, None, None,
                           None, None, None,
                           None] # creating separate frames
        self.frames = [self.addItem, self.deleteItems, self.startPractice, 
                       self.showTerms, self.editTerms, self.makeNewProfile, 
                       self.removeProfile, self.home, self.addBulk,
                       self.deleteBulk, self.noteHome, self.about,
                       self.settings] # storing function for separate frames
        #menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        #filemenu stuff
        filemenu = tk.Menu(self.menubar, tearoff = 0)
        langmenu = tk.Menu(self.menubar, tearoff = 0)
        self.langs = tk.Menu(self.menubar, tearoff = 0)
        bulk = tk.Menu(self.menubar, tearoff = 0)
        abt = tk.Menu(self.menubar, tearoff = 0)
        settings = tk.Menu(self.menubar, tearoff = 0)
        
        filepath = './profiles'
        subdirectories = os.walk(filepath)

        for item in subdirectories:
            for name in item[1]:
                print("name: ", name)
                self.langs.add_command(label = f"Switch to {name}", command = lambda n = name: self.whichToUse(n))
        print("past")

        langmenu.add_command(label = "Add Profiles", command = lambda: self.showFrame('addLang'))
        langmenu.add_command(label = "Remove Profiles", command = lambda: self.showFrame('removeLang'))
        abt.add_command(label = "About Rymn", command= lambda:self.showFrame('about'))
        #filemenu.add_command(label = "Home", command = lambda: self.showFrame('home'))
        filemenu.add_command(label = "Home", command=lambda: self.showFrame('home'))
        filemenu.add_command(label = "Review Terms", command=lambda: self.showFrame('review'))
        filemenu.add_command(label = "Add Terms", command= lambda: self.showFrame('add'))
        bulk.add_command(label = "Bulk Add", command= lambda: self.showFrame('addBulk'))
        filemenu.add_command(label = "Delete Terms", command= lambda: self.showFrame('delete'))
        bulk.add_command(label = "Bulk Delete", command= lambda: self.showFrame('deleteBulk'))
        filemenu.add_command(label = "Edit Terms", command = lambda: self.showFrame('edit'))
        filemenu.add_command(label = "View Terms", command= lambda: self.showFrame('terms'))
        settings.add_command(label = "Adjust Max Term Limit", command= lambda: self.showFrame('termLim'))

        
        
        self.menubar.add_cascade(label = "Go To", menu = filemenu, underline = 0)
        self.menubar.add_cascade(label= "Bulk Operations", menu = bulk, underline = 0)
        self.menubar.add_cascade(label= "Profiles", menu = langmenu, underline = 0)
        self.menubar.add_cascade(label= "Switch Profiles", menu = self.langs, underline = 0)
        self.menubar.add_cascade(label= "About", menu = abt, underline = 0)
        self.menubar.add_cascade(label = "Settings", menu = settings, underline = 0)

        # runs a thread in the background
        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(10)

        # need 2 schedulers, one to handle the every hour update with our review list,
        # and a second one to handle midnight update of dailyLoadUp
        schedule.every().hour.at(":00").do(self.addToReviewList) #first case
        schedule.every().day.at("00:00").do(self.addToDailyLoadUp) #second case
        #schedule.every(5).seconds.do(printTheDailyLoadUp)
        
        # thread handles this so that there's no blocking
        th = threading.Thread(target=run_schedule)
        th.daemon = True
        th.start()

        #code for minimizing window
        def quit_window(icon, item):
            icon.stop()
            self.root.destroy()
        def show_window(icon, item):
            icon.stop()
            self.root.after(0, self.root.deiconify())
        
        def hide_window():
            self.root.withdraw()
            image = PIL.Image.open("rymn.ico")
            menu = (itemzzz('Show', show_window), itemzzz('Quit', quit_window))
            icon = pystray.Icon("Rymn", image, "Rymn", menu)
            icon.run()
        
        self.root.protocol('WM_DELETE_WINDOW', hide_window)
        

        self.root.mainloop()

    def settings(self):
        self.clearFrame()


        def adjust(event):
            global termLimit
            termLimit = (termLimit[0], entry.get())
        frame = tk.Frame(self.root)
        self.framesHold[12] = frame

        lab = tk.Label(self.framesHold[12], text = "Daily New Term Limit", font = ('Louis George Cafe', 18, 'underline'))
        lab.pack()

        entry = tk.Entry(self.framesHold[12])
        entry.pack()

        entry.bind('<Return>', adjust)
        frame.pack()

        return self.framesHold[12]

    def home(self):
        self.clearFrame()
        # prompt
        self.frame = tk.Frame(self.root)
        self.framesHold[7] = self.frame

        note = tk.Label(self.framesHold[7], text = f"If PC goes to sleep, please restart the program!", font = ('Louis George Cafe', 18, 'underline'))
        note.grid(row = 0, column = 0, columnspan=2)

        profile = tk.Label(self.framesHold[7], text = f"Current Profile: {currDir}", font = ('Louis George Cafe', 18))
        profile.grid(row = 1, column = 0, columnspan=2)
        self.prompt = tk.Label(self.framesHold[7], text = f"What would you like to do? ", font = ('Louis George Cafe', 18))
        self.prompt.grid(row = 2, column = 0, columnspan=2)

        # review button
        if len(currReviewList) > 0:
            self.practiceButton = tk.Button(self.framesHold[7] , text = f"Practice {len(currReviewList)} Terms", font = ('Louis George Cafe', 20), command=lambda: self.showFrame('review'))
        else:
            self.practiceButton = tk.Button(self.framesHold[7] , text = f"No Reviews To Do", font = ('Louis George Cafe', 20), command=lambda: self.showFrame('review'))
        self.practiceButton.grid(row = 3, column = 0, columnspan= 4, pady = 5)
        
        #add button
        addItems = tk.Button(self.framesHold[7] , text = "Add Items", font = ('Louis George Cafe', 20), command= self.addItem)
        addItems.grid(row = 4, column= 0, sticky=tk.EW, padx = 10)
        
        #delete button
        deleteItems = tk.Button(self.framesHold[7] , text = "Delete Items", font = ('Louis George Cafe', 20), command = self.deleteItems)
        deleteItems.grid(row = 4, column= 1, sticky=tk.EW)
        

        viewTerms = tk.Button(self.framesHold[7] , text = "View Terms", font = ('Louis George Cafe', 20), command = lambda: self.showFrame('terms'))
        viewTerms.grid(row = 5, column= 0, sticky=tk.EW, padx = 10)

        editItems = tk.Button(self.framesHold[7] , text = "Edit Items", font = ('Louis George Cafe', 20), command = lambda: self.showFrame('edit'))
        editItems.grid(row = 5, column= 1, sticky=tk.EW)

        return self.framesHold[7]
    
    def showFrame(self, frameToDisplay):
        self.clearFrame()
        if self.curr_frame:
            self.curr_frame.pack_forget()
        match frameToDisplay:
                case 'add':
                    self.curr_frame = self.frames[0]()
                case 'delete':
                    self.curr_frame = self.frames[1]()
                case 'review':
                    self.curr_frame = self.frames[2]()
                case 'terms':
                    self.curr_frame = self.frames[3]()
                case 'edit':
                    self.curr_frame = self.frames[4]()
                case 'addLang':
                    self.curr_frame = self.frames[5]()
                case 'removeLang':
                    self.curr_frame = self.frames[6]()
                case 'home':
                    self.curr_frame = self.frames[7]()
                case 'addBulk':
                    self.curr_frame = self.frames[8]()
                case 'deleteBulk':
                    self.curr_frame = self.frames[9]()
                case 'about':
                    self.curr_frame = self.frames[11]()
                case 'termLim':
                    self.curr_frame = self.frames[12]()
        self.curr_frame.pack()

    def about(self):
        frame = tk.Frame(self.root)
        self.framesHold[11] = frame

        titlelabel = tk.Label(self.framesHold[11], text = "About Rymn", font = ('Louis George Cafe', 20, 'underline', 'bold'))
        titlelabel.pack()
        
        def center_wrap(text):
            lines = textwrap.wrap(text)
            return "\n".join(line.center(140) for line in lines)


        text = """Rymn uses a memory based system known as SRS (Spaced Reptition System), to help people memorize vocabulary. This means that once you add a term the more you get it right, the more spaced out the next review for it will be! Review intervals start at four hours and increase until level seven, where terms are reviewed once every few months! Rymn is still in it's infancy and I hope to add many more features as time goes on! Thank you for trying Rymn, if you have any feedback, please email it to \"ahmed2020643@gmail.com!\""""
        aboutlabel = tk.Label(self.framesHold[11], text = center_wrap(text), font = ('Louis George Cafe', 14))
        aboutlabel.pack()

        return self.framesHold[11]

    def removeProfile(self):
        self.clearFrame()
        def remove(event):
            remove = self.entry.get()
            if os.path.exists(f"./profiles/{remove}"):
                shutil.rmtree(f"./profiles/{remove}")
                lab = tk.Label(self.framesHold[6], text = "Removed", font=("Louis George Cafe", 20))
                lab.grid(row = 2, column = 0)
                lab.after(1000, lab.destroy)
                self.langs.delete(f"Switch to {remove}")
            else:
                lab = tk.Label(self.framesHold[6], text = "Couldn't Find Directory!", font=("Louis George Cafe", 20))
                lab.grid(row = 2, column = 0)
                lab.after(1000, lab.destroy)
        frame = tk.Frame(self.root)
        self.framesHold[6] = frame
        label = tk.Label(self.framesHold[6], text = "Which profile do you want to delete?", font=("Louis George Cafe", 20))
        label.grid(row = 0, column = 0)
        self.entry = tk.Entry(self.framesHold[6])
        self.entry.grid(row = 1, column = 0)
        self.entry.bind('<Return>', remove)
        frame.pack()

        return self.framesHold[6]
    
    def makeNewProfile(self):
        self.clearFrame()
        def makeProfile(event):
            profileName = self.entry.get()
            subdir = os.walk('./profiles')
            add_to_list = True
            for item in subdir:
                for name in item[1]:
                    if name == profileName:
                        add_to_list = False
            
            if add_to_list == True:   
                self.langs.add_command(label = f"Switch to {profileName}", command = lambda n = profileName: self.whichToUse(n))
                os.mkdir(f"./profiles/{profileName}")
                print("here")
                lbl = tk.Label(self.framesHold[5], text = "Profile Added!", font = ('Louis George Cafe', 20))
                lbl.pack()
                lbl.after(1000, lbl.destroy)
            else:
                print("ouch")
                lbl = tk.Label(self.framesHold[5], text = "Cannot make two profiles with the same name!", font = ('Louis George Cafe', 20))
                lbl.pack()
                lbl.after(1000, lbl.destroy)
        frame = tk.Frame(self.root)
        self.framesHold[5] = frame
        label = tk.Label(self.framesHold[5], text = "What is the name of the new profile?", font = ('Louis George Cafe', 20))
        label.pack()
        self.entry = tk.Entry(self.framesHold[5])
        self.entry.bind('<Return>', makeProfile)
        self.entry.pack()
        
    
        return self.framesHold[5]
    
    def whichToUse(self, nameOfPath):
        print(f"switching to profile {nameOfPath}")
        needToBeCreated = True
        
        
        filepath = './profiles'
        subdirectories = os.walk(filepath)
        for item in subdirectories:
            for name in item[1]:
                if nameOfPath == name:
                    needToBeCreated = False
        global itemFinder
        global dailyLoadUp
        global currReviewList
        if needToBeCreated:
            os.mkdir(f"./profiles/{nameOfPath}")

        else:
            global previousDirect
            global currDir
            
            print("previous directory: ", previousDirect)
            if previousDirect != nameOfPath and previousDirect:
                with open(f"./profiles/{previousDirect}/itemFinderOut", "wb") as outfile:
                    print("itemFinders prev ",itemFinder)
                    pickle.dump(itemFinder, outfile)
                with open(f"./profiles/{previousDirect}/dailyOut", "wb") as outfile:
                    # print("loadups: prev", dailyLoadUp)
                    pickle.dump(dailyLoadUp, outfile)
                with open(f"./profiles/{previousDirect}/currReviewOuts", "wb") as outfile:
                    # print("rev: prev", currReviewList)
                    pickle.dump(currReviewList, outfile)
                with open(f"./profiles/{previousDirect}/termLim", "wb") as outfile:
                    # print("rev: prev", currReviewList)
                    pickle.dump(termLimit, outfile)
            previousDirect = nameOfPath
            currDir = nameOfPath
            # dumping current directory files to be read
            if os.path.exists(f"./profiles/{nameOfPath}/itemFinderOut") == False:
                with open(f"./profiles/{nameOfPath}/itemFinderOut", "wb") as outfile:
                    print("itemFinders ",itemFinder)
                    x = {"0": [], 
                            "1": [],
                            "2": [],
                            "3": [],
                            "4": [],
                            "5": [],
                            "6": [],
                            "7": []
                            }
                    pickle.dump(x, outfile)
                with open(f"./profiles/{nameOfPath}/dailyOut", "wb") as outfile:
                    # print("loadups: ", dailyLoadUp)
                    x = {
                        "0": [],
                        "1": [],
                        "2": [],
                        "3": [],
                        "4": [],
                        "5": [],
                        "6": [],
                        "7": [],
                        "8": [],
                        "9": [],
                        "10": [],
                        "11": [],
                        "12": [],
                        "13": [],
                        "14": [],
                        "15": [],
                        "16": [],
                        "17": [],
                        "18": [],
                        "19": [],
                        "20": [],
                        "21": [],
                        "22": [],
                        "23": []
                    }
                    pickle.dump(x, outfile)
                with open(f"./profiles/{nameOfPath}/currReviewOuts", "wb") as outfile:
                    # print("rev: ", currReviewList)
                    pickle.dump([], outfile)
                with open(f"./profiles/{nameOfPath}/termLim", "wb") as outfile:
                    # print("rev: ", currReviewList)
                    pickle.dump((datetime.date, 30), outfile)
            # using curr direct files
            print(f"currently writing to {nameOfPath}")
            with open(f"./profiles/{nameOfPath}/itemFinderOut", "rb") as infile:
                itemFinder = pickle.load(infile)
            with open(f"./profiles/{nameOfPath}/dailyOut", "rb") as infile:
                dailyLoadUp = pickle.load(infile)
            with open(f"./profiles/{nameOfPath}/currReviewOuts", "rb") as infile:
                currReviewList = pickle.load(infile)
            with open(f"./profiles/{nameOfPath}/termLim", "rb") as infile:
                termLimit = pickle.load(infile)
            # dumping previous directory files
        self.addToDailyLoadUp()
        self.checkReviewsOnStartup()
        self.showFrame('home')
                

    def clearFrame(self):
        self.btn_frame.destroy()
        # self.prompt.destroy()
        if self.curr_frame:
            self.curr_frame.destroy()
        #self.frame.destroy()

    def listItemFinder(self):
        l = []
        for lvl in itemFinder:
            l.extend(itemFinder[lvl])
        return l
    
    def checkReviewsOnStartup(self):
        now = datetime.now()
        i = 0
        addToRev = True
        # goes through and checks if items need to be added to reviewList, 
        # if they're not already in it
        print("DAILY LOAD UP IN CHECK REVIEWS: ", dailyLoadUp)
        while i <= now.hour:
            for item in dailyLoadUp[str(i)]:
                for itemRev in currReviewList:
                    if item.item_name == itemRev.item_name:
                        addToRev = False
                if addToRev == True:
                    print("item: ", item)
                    currReviewList.append(item)
                addToRev = True
            dailyLoadUp[str(i)] = []
            i+=1

    def addToReviewList(self):
        now = datetime.now()
        addToList = True
        #adding to review list, and removing from dailyLoadUp      
        for item in dailyLoadUp[str(now.hour)]:
            for itemRev in currReviewList:
                if item.item_name == itemRev.item_name:
                    addToList == False
            if addToList: currReviewList.append(item)
            addToList = True
        dailyLoadUp[str(now.hour)] = []
        # if len(currReviewList) != 0:
        notification.notify(
                title = 'RYMN',
                message = f"You have {len(currReviewList)} reviews to do!",
                app_icon = "rymn.ico",
                timeout = 10
            )
        print("review list: ", currReviewList, "time: ", now.strftime("%d/%m/%Y %H:%M:%S"))

    def addToDailyLoadUp(self):
        now = datetime.now()
        #curr_date = now.strftime("%d/%m/%Y %H:%M:%S")
        #adding to the applicable hour
        in_list = False
        for item in self.listItemFinder():
            item_date = datetime.strptime(item.date_to_review, "%d/%m/%Y")
            if item_date.date() == now.date():
                print("date to review: ", item_date)
                for itemInDaily in dailyLoadUp[str(item.hour_to_review)]:
                    if itemInDaily.item_name == item.item_name:
                        in_list = True
                
                if in_list == False: dailyLoadUp[str(item.hour_to_review)].append(item)
            elif item_date.date() < now.date():
                print("previous days")
                # add to 0
                for itemInDaily in dailyLoadUp[str("0")]:
                    if itemInDaily.item_name == item.item_name:
                        in_list = True
                if in_list == False: dailyLoadUp["0"].append(item)
            in_list = False
        

    # this should show a grid of terms and when each term is hovered over, 
    # it should show the definition as well as the date and time of the review
    def showTerms(self):
        self.clearFrame()
        countx= 0
        county=0
        frame = tk.Frame(self.root)
        self.framesHold[3] = frame    
        frame.pack(fill=BOTH, expand = 1)

        my_canvas = Canvas(self.framesHold[3])
        

        yscrollbar = Scrollbar(self.framesHold[3], orient = VERTICAL, command = my_canvas.yview)
        yscrollbar.pack(side = RIGHT, fill = Y)

        xscrollbar = Scrollbar(self.framesHold[3], orient = HORIZONTAL, command = my_canvas.xview)
        xscrollbar.pack(side = BOTTOM, fill = 'x')

        my_canvas.configure(yscrollcommand=yscrollbar.set)
        my_canvas.configure(xscrollcommand=xscrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


        frame2 = tk.Frame(my_canvas)

        

        for item in self.listItemFinder():
            
            if county == 14:
                county = 0
                countx+=1
            label = tk.Label(frame2, text = item.item_name, font = ('Louis George Cafe', 16), borderwidth = 1, relief = "raised")
            label.grid(row = countx, column = county, padx = 1, sticky= tk.EW)  
            county +=1
            tooltip_t = f"Definition: {item.item_definition}\nNext review: {item.date_to_review} {item.hour_to_review}\nAlternate Definition: {item.alternate_definitions}"
            CreateToolTip(label, tooltip_t)

        
        my_canvas.create_window((0,0), window=frame2, anchor = "nw")
        my_canvas.config(width=frame2.winfo_width(), height=frame2.winfo_height())  
        my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)
        return frame


 ################# START OF PRACTICE #################
    def startPractice(self):
        self.clearFrame()
        # getting current hour
        print("DAILY LOAD: ", dailyLoadUp)
        print("REVIEW LIST: ", currReviewList)
        self.frame_practice = tk.Frame(self.root)
        self.framesHold[0] = self.frame_practice
        
        # reviewing all items for hour
        if len(currReviewList) == 0:
            nothing = tk.Label(self.frame_practice, text = "Nothing to review!", font = ('Louis George Cafe', 20))
            nothing.grid(row = 0, column = 0)
            print("nothing to do!")
        else:
            self.itemx = random.choice(currReviewList)
            prompt = tk.Label(self.frame_practice, text = f"Definition of {self.itemx.item_name}?", font = ('Louis George Cafe', 16))
            prompt.grid(row = 0, column = 0, sticky=tk.EW)
            self.answerBox = tk.Entry(self.frame_practice)
            self.answerBox.grid(row = 1, column = 0, sticky=tk.EW)
            
            self.count = 0
            
            if self.count == 0: 
                self.answerBox.bind('<Return>', self.checkItemCorrect)
                print("selfie: ",self.count)
                
            #print("itemx: ", self.itemx)
            
        self.frame_practice.pack()
        self.clearFrame()
        return self.frame_practice

    def hey(self, event):
        print("hello")
    def checkItemCorrect(self, event):
        self.count+=1
        self.answerBox.configure(state="disabled")
        self.answerBox.bind('<Return>', self.hey)
        self.answer = self.answerBox.get()
        answer = self.answer
        self.correctState = None
        
        print("in check item correct")
        # correct case
        itemFound = False
        for item in self.itemx.alternate_definitions:
            if answer.lower() == item.lower():
                itemFound == True
        

        if answer.lower() == self.itemx.item_definition.lower() or itemFound:
            self.correctState = True
            # Fixing level
            print("CORRECT!")
            if self.itemx.gotten_wrong == False: 
                self.itemx.previous_item_lvl = self.itemx.item_level
                print("ADDED A LEVEL!")
                print("previous level: ", self.itemx.item_level)
                print("here in right", self.itemx)
                itemInt = int(self.itemx.item_level)
                itemInt+=1
                self.itemx.item_level = str(itemInt)

            # Updating time for next review
            (date, hour) = HelperMethods.getNewHoursForItem(self.itemx)
            self.itemx.updateHoursAndTime(date, hour)
            
            # if we get it right, we dont need to review it again
            for item in currReviewList:
                if item.item_name == self.itemx.item_name: 
                    currReviewList.remove(item)
            

        # wrong case
        else:
            self.correctState = False
            
            # decreasing level by 1 and can only decrease once
            if int(self.itemx.item_level) > 0 and self.itemx.gotten_wrong == False:
                print("WRONG!!!!")
                print("previous level: ", self.itemx.item_level)
                print("here in wrong", self.itemx)
                self.itemx.previous_item_lvl = self.itemx.item_level
                itemInt = int(self.itemx.item_level)
                itemInt-=1
                self.itemx.item_level = str(itemInt)
            self.itemx.gotten_wrong = True
            # remove the term from our currReviewList and then we
            # add the new adjusted term to our reviewList again!
            for item in currReviewList:
                if item.item_name == self.itemx.item_name:
                    currReviewList.remove(item)
            # Updating time for next reviewe
            (date, hour) = HelperMethods.getNewHoursForItem(self.itemx)
            self.itemx.updateHoursAndTime(date, hour)
            currReviewList.append(self.itemx)
        self.displayCorrectOrIncorrect()
            

    def displayCorrectOrIncorrect(self):
        # incorrect
        print("in displayCorrectOrIncorrect")
        if self.correctState == False:
            definitionLabel = tk.Label(self.frame_practice, text = f"Wrong! Correct definition is {self.itemx.item_definition}")
            definitionLabel.grid()
            nextButton = tk.Button(self.frame_practice, text = "Next", font = ('Louis George Cafe', 10), command = lambda: self.showFrame('review'))
            nextButton.grid() 
        else:
            correct = tk.Button(self.frame_practice, text = "Correct!", font = ('Louis George Cafe', 16), command = self.updateTermAfterReview)
            correct.grid()

    def updateTermAfterReview(self):
        # need to update in itemFinder, allTerms:
        # updating itemFinder
        print("in updateTermAfterReview")
        print("curr self.itemx", self.itemx)
        print("previous level: ", str(self.itemx.previous_item_lvl))
        print("previousLevelList: ", itemFinder[str(self.itemx.previous_item_lvl)])
        print("all of itemFinders: ", self.listItemFinder())
        self.itemx.gotten_wrong = False
        for item in self.listItemFinder():
            if item.item_name == self.itemx.item_name: # found the term
                print("our new item is: ", self.itemx)
                print("our old item was: ", item)  
                if self.itemx.item_level == str(self.itemx.previous_item_lvl):
                    print("sus case")
                    itemFinder[self.itemx.item_level].remove(item)
                    itemFinder[self.itemx.item_level].append(self.itemx)                    
                else:
                    print("we just removed and added")
                    itemFinder[self.itemx.previous_item_lvl].remove(item)
                    itemFinder[self.itemx.item_level].append(self.itemx)
        
        self.showFrame('review')

####################### END OF PRACTICE ###########################
####################### START OF ADD ############################
    # Adds the item, and makes it be reviewed in 4 hours (lvl 0)
    def addItem(self):
        self.clearFrame() 
             
        
        self.frameAdd = tk.Frame(self.root)
        self.curr_frame = self.frameAdd
        # for term
        new_frame = tk.Frame(self.frameAdd)
        term_label = tk.Label(new_frame, text = "Please enter the term you would like to add", font = ('Louis George Cafe', 16))
        term_label.grid(row = 0, column=0, sticky=W, padx = (0, 10))
        self.t_entry = tk.Entry(new_frame)
        self.t_entry.grid(row = 0, column=1, sticky=EW)

        # for defn
        defn_label = tk.Label(new_frame, text = "Please enter the definition of the term", font = ('Louis George Cafe', 16))
        defn_label.grid(row = 1, column = 0, sticky=EW)
        self.d_entry = tk.Entry(new_frame)
        self.d_entry.grid(row = 1, column=1, sticky=EW)
        new_frame.pack()
        
        self.d_entry.bind('<Return>', self.mediatorAdd)
        
        # confirmation
        self.button_confirm = tk.Button(self.frameAdd, text = "Add Item", font = ('Louis George Cafe', 16), command = self.addEntries)
        self.button_confirm.pack()
        self.frameAdd.pack()

        return self.frameAdd
    
    def mediatorAdd(self, event):
        self.addEntries()
    def addEntries(self):
        self.term_entry = self.t_entry.get()
        self.defn_entry = self.d_entry.get()
        add_item = True
        
        for item in self.listItemFinder():
            if item.item_name == self.term_entry:
                add_item = False
        
        if add_item:
            addedLabel = tk.Label(self.frameAdd, text = "Added!", font = ('Louis George Cafe', 16))
            addedLabel.pack()
            addedLabel.after(1000, addedLabel.destroy)


            term = self.term_entry
            full_defn = self.defn_entry
            defn = re.findall("(\w+[^,]*)+", full_defn)
            
            alt_defn = re.findall("(\w+[^,]*)+", full_defn)
            
            defn = defn[:1]
            defnt = None
            for item in defn:
                defnt = item

            print("defn: ", defnt)
            alt_defn = alt_defn[1:]
            nl = [x for x in alt_defn]
            
            
            item_to_add = Item(term, defnt, nl)


            # getting date and time for next review
            now = datetime.now()
            now = now+timedelta(hours = 4)
            reviewstr = now.strftime("%d/%m/%Y %H:%M:%S")
            item_to_add.date_to_review = re.search("\d{1,2}/\d{1,2}/\d{4}", reviewstr).group()
            item_to_add.hour_to_review = int(re.search(" \d{1,2}", reviewstr).group())

            # set the new time, set the date, add it to our list of terms.
            #allTerms.add(item_to_add)
            itemFinder['0'].append(item_to_add)
            termLimit = termLimit(termLimit[0], termLimit[1]+1)
        else:
            notAddedLabel = tk.Label(self.frameAdd, text = "Already have a term with that name!", font = ('Louis George Cafe', 16))
            notAddedLabel.pack()
            notAddedLabel.after(1000, notAddedLabel.destroy)

################## END OF ADD ######################
################## START OF DELETE #####################

    # Deletes the item from all of our lists
    def deleteItems(self):
        self.clearFrame()
        
        frame = tk.Frame(self.root)
        self.framesHold[1] = frame
        
        self.curr_frame = frame
        qLabel = tk.Label(self.framesHold[1], text = f"What is the term you want to delete?", font = ('Louis George Cafe', 20))
        qLabel.grid(row = 0, column = 0)

        entryLabel = tk.Entry(self.framesHold[1])
        entryLabel.grid(row = 2, column = 0, sticky = tk.EW)
        self.term_entry = entryLabel
        self.searchButton = tk.Button(self.framesHold[1], text = f"Search!", font = ('Louis George Cafe', 20), command = self.getEntryItem)
        self.searchButton.grid(row = 0, column = 1, padx= 10, rowspan=3)
        
        frame.pack()

        return frame

    def getEntryItem(self):
        deleteItem = None
        self.searchButton.configure(state = "disabled")
        # need to remove from allTerms, itemFinder, termsAndDefns, and possibly dailyLoadUp
        def delete(): 
            self.button.configure(state = "disabled")
            deletedLabel = tk.Label(self.framesHold[1], text = "Deleted!", font = ('Louis George Cafe', 20))
            deletedLabel.grid()
                 
            currdate = item_to_delete.date_to_review
            currdate = re.search("\d{1,2}/\d{1,2}/\d{4}", currdate)
            
            deletedLabel.after(1000, deletedLabel.destroy)
            self.button.after(1000, self.button.destroy)

            #finding exact term
            termx = None
            for item in itemFinder[deleteItem.item_level]:
                if item.item_name == deleteItem.item_name:
                    termx = item
            

            #if dates are the same remove from today's lineup
            if currdate.group() == (re.search("\d{1,2}/\d{1,2}/\d{4}", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))).group():
                dailyLoadUp[str(deleteItem.hour_to_review)]

            #allTerms.discard(deleteItem)
            itemFinder[deleteItem.item_level].remove(termx)
            if deleteItem in currReviewList:
                currReviewList.remove(deleteItem)
            self.searchButton.configure(state = "normal")
        itemToFind = self.term_entry.get()
        termx = False

        # removing from itemFinder
        for item_to_delete in self.listItemFinder():
            if item_to_delete.item_name == itemToFind:
                deleteItem = item_to_delete
                self.button = tk.Button(self.framesHold[1], text = f"Delete {itemToFind}", font = ('Louis George Cafe', 20), command = delete)
                self.button.grid(pady=(5,0))
                self.framesHold[1].pack()
                termx = True
        # remvoing from daily load up
        for item in dailyLoadUp:
            for itemx in dailyLoadUp[item]:
                if itemx.item_name == item_to_delete.item_name:
                    dailyLoadUp[item].remove(itemx)
        # removing from review list
        for item in currReviewList:
            if item.item_name == item_to_delete.item_name:
                currReviewList.remove(item)
        if termx == False:
            label = tk.Label(self.framesHold[1], text = "Term Not Found", font = ('Louis George Cafe', 20))
            label.grid()
            label.after(1000, label.destroy)
            self.searchButton.configure(state = "normal")
        return self.framesHold[1]     
        
####################### END OF DELETE #######################
####################### START OF EDIT #######################
    def findTerm(self, term_to_find):
        for item in self.listItemFinder():
            if item.item_name == term_to_find:
                return item
    
    def editTerms(self):
        self.clearFrame()
        
        self.can_be_clicked = True
        self.eFrame = tk.Frame(self.root)
        self.framesHold[2] = self.eFrame

        self.curr_frame = self.eFrame
        qLabel = tk.Label(self.framesHold[2], text = "What term do you want to edit?", font = ('Louis George Cafe', 20))
        qLabel.grid(row = 0, column = 0)
        
        self.entryLabel = tk.Entry(self.framesHold[2])
        self.entryLabel.grid(row = 2, column = 0, sticky = tk.EW)
        
        if self.can_be_clicked: 
            self.searchButton = tk.Button(self.framesHold[2], text = "Search!", command = self.editTermInternal, font = ('Louis George Cafe', 20))
            
        self.searchButton.grid(row = 0, column = 1, padx = 10, rowspan = 3, sticky = tk.NSEW)

        self.eFrame.pack()
        return self.eFrame
    
    def editTermInternal(self):
        self.searchButton.configure(state = "disabled")
        self.can_be_clicked = False
        self.item_edit = self.entryLabel.get()
        item_to_e = None
        print("in item finder here 222222222222222222222222")
        print("itemssss", self.item_edit)
        def edit():
            self.can_be_clicked = False
            for item in itemFinder[item_to_e.item_level]:
                if item.item_name == item_to_e.item_name:
                    print("FOUND YOU!!!!", item)
                    itemFinder[item_to_e.item_level].remove(item)
            answer = self.dEntry.get()
            print("ABNSWERRR", answer)
            defn = re.search("^\w+", answer).group()
            alt_defn = re.findall("\w+(?:\s+\w+)*", answer)

            alt_defn = alt_defn[1:]
            nl = []
            for item in alt_defn: 
                nl.append(" ".join(item.split()))


            item_to_e.item_definition = defn
            item_to_e.alternate_definitions = nl
            print("ITEM TO E", item_to_e)
            itemFinder[item_to_e.item_level].append(item_to_e)
            self.dEntry.after(1000, self.dEntry.destroy)
            self.dLabel.after(1000, self.dLabel.destroy)
            self.eButton.after(1000, self.eButton.destroy)
            self.searchButton.configure(state = "normal")
            print(item_to_e)
        for item in self.listItemFinder():
            if item.item_name == self.item_edit:
                print("in item finder here")
                item_to_e = item
                self.dLabel = tk.Label(self.framesHold[2], text = "What do you want the new definition to be?", font = ('Louis George Cafe', 20))
                self.dLabel.grid(row = 2, column = 0)
                
                self.dEntry = tk.Entry(self.framesHold[2])
                self.dEntry.grid(row = 2, column = 1)
                
                
                self.eButton = tk.Button(self.framesHold[2], text = "Edit!", command = edit)
                
                
                self.dEntry.get()
                self.eButton.grid()
        self.framesHold[2].pack()
        return self.framesHold[2]

    ##################### ADD IN BULK ###################
    def addBulk(self):
        def add():
            # adding terms
            termTxt = self.termBox.get(1.0, "end-1c")
            defnTxt = self.defnBox.get(1.0, "end-1c")

            termsList = re.findall("(.+)+", termTxt)
            defnsList = re.findall("(.+)+", defnTxt)

            global termLimit
            if len(termsList) > termLimit[1]:
                lab = tk.Label(self.framesHold[8], text = "Terms added exceed daily limit, please adjust!", font = ('Louis George Cafe', 14))
                lab.pack()

            elif len(termsList) == len(defnsList):
                now = datetime.now()
                now = now+timedelta(hours = 4)
                nowMinusFour = datetime.now()
                reviewstr = now.strftime("%d/%m/%Y %H:%M:%S")
                i = 0
                allTerms = self.listItemFinder()
                print("all terms: ", allTerms)
                # fix mulitple items being added with same name !!!!!!!!!!!!!!!!!!!! FIXXXXXXXX
                while i < len(termsList):
                    print("termList[i]", termsList[i])
                    addToList = True
                    for item_n in allTerms:
                        if item_n.item_name == termsList[i]:
                            addToList = False
                    if addToList == True:
                        full_defn = defnsList[i]
                        defn = re.findall("(\w+[^,]*)+", full_defn)
                        alt_defn = re.findall("(\w+[^,]*)+", full_defn)

                        defn = defn[:1]
                        defnt = None
                        for item in defn:
                            defnt = item
                        
                        print("Defn: ", defnt)
                        alt_defn = alt_defn[1:]
                        nl = [x for x in alt_defn]

                        itemToAdd = Item(termsList[i], defnt, nl)
                        itemToAdd.date_to_review = re.search("\d{1,2}/\d{1,2}/\d{4}", reviewstr).group()
                        itemToAdd.hour_to_review = int(re.search(" \d{1,2}", reviewstr).group())
                        # adding into item finder
                        allTerms.append(itemToAdd)
                        itemFinder["0"].append(itemToAdd)

                        # if applicable add it into dailyLoadUp
                        if now.date() == nowMinusFour.date():
                            dailyLoadUp[str(itemToAdd.hour_to_review)].append(itemToAdd)

                    i+=1
                lab = tk.Label(self.framesHold[8], text = "Added!", font = ('Louis George Cafe', 18))
                lab.pack()
                lab.after(1000, lab.destroy)
                termLimit = termLimit(termLimit[0], termLimit[1]+len(termsList))
            else:
                lab = tk.Label(self.framesHold[8], text = "Terms and definitions are mismatched!", font = ('Louis George Cafe', 18))
                lab.pack()
                lab.after(1000, lab.destroy)
        frame = tk.Frame(self.root)
        self.framesHold[8] = frame
        
        tLabel = tk.Label(self.framesHold[8], text = "Please enter the terms you want to add, separated by an enter.", font = ('Louis George Cafe', 18))
        tLabel.pack()
        
        hscroll = Scrollbar(self.framesHold[8], orient = 'vertical')
        vscroll = Scrollbar(self.framesHold[8], orient = 'horizontal')
        self.termBox = tk.Text(self.framesHold[8], yscrollcommand=vscroll.set, xscrollcommand=hscroll.set, width = 100, height = 20)
        self.termBox.pack()

        self.dLabel = tk.Label(self.framesHold[8], text = "Please enter definitions of the terms you want to add, separated by an enter.", font = ('Louis George Cafe', 18))
        self.dLabel.pack()
        self.defnBox = tk.Text(self.framesHold[8], yscrollcommand=vscroll.set, xscrollcommand=hscroll.set , width = 100, height = 20)
        self.defnBox.pack()

        addButton = tk.Button(self.framesHold[8], text = "Add Items!", font = ('Louis George Cafe', 18), command = add)
        addButton.pack()
        return self.framesHold[8]
    
    ####### DELETE IN BULK ############# 
    def deleteBulk(self):
        def delete():
            # adding terms
            termTxt = self.termBox.get(1.0, "end-1c")
            termsList = re.findall("(.+)+", termTxt)
            now = datetime.now()

            i = 0
            allTerms = self.listItemFinder()

            while i < len(termsList):
                itemToRemove = None
                for item in allTerms:
                    if item.item_name == termsList[i]:
                        itemToRemove = item
                if itemToRemove:
                    itemFinder[itemToRemove.item_level].remove(itemToRemove)

                    # if applicable add it into dailyLoadUp
                    if now.date() == itemToRemove.date_to_review:
                        dailyLoadUp[str(itemToRemove.hour_to_review)].remove(itemToRemove)

                    
                    if itemToRemove in currReviewList:
                        currReviewList.remove(itemToRemove)
                    
                i+=1
            lab = tk.Label(self.framesHold[9], text = "Removed!", font = ('Louis George Cafe', 18))
            lab.pack()
            lab.after(1000, lab.destroy)
        frame = tk.Frame(self.root)
        self.framesHold[9] = frame
        
        tLabel = tk.Label(self.framesHold[9], text = "Please enter the terms you want to delete, separated by an enter.", font = ('Louis George Cafe', 18))
        tLabel.pack()
        
        hscroll = Scrollbar(self.framesHold[9], orient = 'vertical')
        vscroll = Scrollbar(self.framesHold[9], orient = 'horizontal')
        self.termBox = tk.Text(self.framesHold[9], yscrollcommand=vscroll, xscrollcommand=hscroll, width = 100, height = 20)
        self.termBox.pack()

        delButton = tk.Button(self.framesHold[9], text = "Delete Items!", font = ('Louis George Cafe', 18), command = delete)
        delButton.pack()
        return self.framesHold[9]
    
    ########## START OF NOTES ###########
    def noteHome(self):
        
        self.clearFrame()
        frame = tk.Frame(self.root)
        self.framesHold[10] = frame
        
        label = tk.Label(self.framesHold[10], text = "What would you like to do?", font = ('Louis George Cafe', 18))
        label.grid(row = 0, sticky=tk.EW)

        addButton = tk.Button(self.framesHold[10], text = "Add a Topic", font = ('Louis George Cafe', 18), command = self.addTopic)
        addButton.grid(row = 1, column = 0)

        # for topics in notes:
        #     topic = tk.Button(self.framesHold[10], text = ""






    
class HelperMethods:
    # Returns a tuple with the new date (string) and time (int) for the item
    def getNewHoursForItem(item):
        now = datetime.now()
        if item.item_level == "0":
            print("lvl 0")
            new_now = now+timedelta(hours = 4)
        elif item.item_level == "1":
            print("lvl 1")
            new_now = now+timedelta(hours = 8)
        elif item.item_level == "2":
            print("lvl 2")
            new_now = now+timedelta(hours = 24)
        elif item.item_level == "3":
            print("lvl 3")
            new_now = now+timedelta(hours = 48)
        elif item.item_level == "4":
            print("lvl 4")
            new_now = now+timedelta(hours = 168)
        elif item.item_level == "5":
            print("lvl 5")
            new_now = now+timedelta(hours = 336)
        elif item.item_level == "6":
            print("lvl 6")
            new_now = now+timedelta(hours = 730)
        else:
            print("lvl 7")
            new_now = now+timedelta(hours = 2920)
        
        dt_string = new_now.strftime("%d/%m/%Y %H:%M:%S")
        new_date = re.search("\d{1,2}/\d{1,2}/\d{4}", dt_string)
        new_date = new_date.group()
        return (new_date, new_now.hour)

# Loading up the main GUI, and when the program is closed,
# serialize all the data to make sure it's saved using pickle
try:
    print(re.sub("\s\s+", " ", "hahah    magha"))
    MainGUI()
finally:
    with open(f"./profiles/{previousDirect}/itemFinderOut", "wb") as outfile:
        print("itemFinders ",itemFinder)
        pickle.dump(itemFinder, outfile)
    with open(f"./profiles/{previousDirect}/dailyOut", "wb") as outfile:
        print("loadups: ", dailyLoadUp)
        pickle.dump(dailyLoadUp, outfile)
    with open(f"./profiles/{previousDirect}/currReviewOuts", "wb") as outfile:
        print("rev: ", currReviewList)
        pickle.dump(currReviewList, outfile)
