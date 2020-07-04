#imports
from tkinter import Tk, Frame, Listbox, Label, Button, Menu, Scrollbar, messagebox, filedialog, RIGHT, LEFT, BOTH, BROWSE, Y, END
from prompts import AddPerson, EditPerson, DocsWindow, ExportWindow
import datetime

#class
class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.user = "GUEST"
        self.theme = 1
        self.themeColours = {
            1:["white"],
            -1:["#9c9c9c"]
        }
        self.title("Phonebook 2 ({})".format(self.user))
        self.geometry("300x250")
        self.resizable(width = False, height = False)
        self.phonebook_list = []
        self.months = {"01":"January", "02":"February", "03":"Maarch", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November", "12":"December"}
        
        self.addPrompt = None
        self.editPrompt = None
        self.exportWindow = None
        self.docsWindow = None

        #Widgets:
        self.rightFrame = Frame()
        self.rightFrame.pack(side=RIGHT)

        self.leftFrame = Frame()
        self.leftFrame.pack(side=LEFT)


        self.yscrollbar = Scrollbar(self.leftFrame)
        self.phonebook = Listbox(self.leftFrame, height = 15, selectmode = BROWSE, yscrollcommand = self.yscrollbar.set)
        self.yscrollbar.config(command = self.phonebook.yview)
        self.yscrollbar.pack(fill = Y, side = RIGHT)
        self.phonebook.pack(fill= BOTH, side = LEFT)


        self.introLabel = Label(self.rightFrame, text = "Signed in as {}".format(self.user))
        self.introLabel.pack()

        self.today = str(datetime.date.today()).split("-")
        self.dateLabel = Label(self.rightFrame, text = "{} {}, {}".format(self.today[2], self.months[self.today[1]], self.today[0]))
        self.dateLabel.pack()


        self.buttonsFrame = Frame(self.rightFrame)
        self.buttonsFrame.pack()

        self.addButton = Button(self.buttonsFrame, text = "Add", width = 5, command = self.add)
        self.addButton.pack()

        self.delButton = Button(self.buttonsFrame, text = "Delete", width = 5, command = self.delete)
        self.delButton.pack()

        self.editButton = Button(self.buttonsFrame, text="Edit", width=5, command=self.edit)
        self.editButton.pack()

        self.resetButton = Button(self.buttonsFrame, text="Reset", width=5, command=self.reset)
        self.resetButton.pack()

        self.importButton = Button(self.buttonsFrame, text = "Import", width = 5, command = self.imp)
        self.importButton.pack()

        self.exportButton = Button(self.buttonsFrame, text="Export", width = 5, command = self.exp)
        self.exportButton.pack()

        self.docsButton = Button(self.buttonsFrame, text="Docs", width = 5, command = self.docs)
        self.docsButton.pack()

        #Create menus and bind
        self.createMenus()
        self.createShortcuts()

        #Protocol
        self.protocol("WM_DELETE_WINDOW", self.close)

    def createMenus(self):
        self.mainMenubar = Menu()
        self.config(menu = self.mainMenubar)

        self.mainCascade = Menu(self.mainMenubar)
        self.mainMenubar.add_cascade(label = "Your Phonebook", menu = self.mainCascade)
        self.mainCascade.add_command(label = "Add person", command = self.add, accelerator = "Ctrl+A")
        self.mainCascade.add_command(label = "Delete person", command = self.delete, accelerator = "Ctrl+D")
        self.mainCascade.add_command(label="Edit person", command = self.edit, accelerator = "Ctrl+E")
        self.mainCascade.add_command(label="Reset phonebook", command = self.reset, accelerator = "Ctrl+R")
        self.mainCascade.add_command(label="Switch theme", command = self.toggleTheme, accelerator = "Ctrl+T")
        self.mainCascade.add_separator()
        self.mainCascade.add_command(label="Import", command = self.imp)
        self.mainCascade.add_command(label="Export", command = self.exp)

        self.aboutCascade = Menu(self.mainMenubar)
        self.mainMenubar.add_cascade(label = "About", menu = self.aboutCascade)
        self.aboutCascade.add_command(label="Phonebook 2")
        self.aboutCascade.add_command(label="Released 2/07/2020")
        self.aboutCascade.add_separator()
        self.aboutCascade.add_command(label = "Docs", command = self.docs)

    def createShortcuts(self):
        self.bind_all("<Control-a>", self.add) #ctrl a
        self.bind_all("<Control-d>", self.delete) #ctrl d
        self.bind_all("<Control-e>", self.edit) #ctrl e
        self.bind_all("<Control-r>", self.reset)  # ctrl r
        self.bind_all("<Control-t>", self.toggleTheme) #ctrl t


    def add(self, event = 0):
        if not self.addPrompt is None:
            self.addPrompt.destroy()

        self.addPrompt = AddPerson(self)
        self.addPrompt.mainloop()

    def delete(self, event = 0):
        if self.phonebook.curselection() == ():
            messagebox.showerror("Invalid usage", "Please select an element from the list first to delete it.")

        else:
            self.phonebook_list.remove(self.phonebook_list[self.phonebook.curselection()[0]])
            self.phonebook.delete(self.phonebook.curselection()[0])

    def edit(self, event = 0):
        if not self.editPrompt is None:
            self.editPrompt.destroy()

        if self.phonebook.curselection() == ():
            messagebox.showerror("Invalid usage", "Please select an element from the list first to edit it.")

        else:
            self.editPrompt = EditPerson(self)

    def reset(self, event = 0):
        if self.phonebook_list == []:
            messagebox.showerror("Phonebook already empty", "The phonebook is already empty.")
        
        else:
            if messagebox.askyesno("Confirm", "Are you sure you want to reset your phonebook?"):
                self.phonebook_list = []
                self.phonebook.delete(0, END)
                self.update_user("GUEST")


    def imp(self, event = 0):
        path = filedialog.askopenfilename()
        file = open(path, "r").read().splitlines()
        file.remove(file[len(file)-1])

        self.update_user(file[0])
        self.phonebook.delete(0, END)

        file.remove(file[0])
        file.remove(file[0])

        for i in file:
            self.phonebook_list.append(i)
            self.phonebook.insert(END, i)

    def exp(self, event = 0):
        if self.phonebook_list == []:
            messagebox.showerror("Phonebook empty", "You cannot export an empty phonebook.")

        else:
            if not self.exportWindow is None:
                self.exportWindow.destroy()

            self.exportWindow = ExportWindow(self)
            self.exportWindow.mainloop()

    def docs(self, event = 0):
        if not self.docsWindow is None:
            self.docsWindow.destroy()
        
        self.docsWindow = DocsWindow(self)
        self.docsWindow.mainloop()

    def update_user(self, user):
        self.user = user
        self.title("Phonebook 2 ({})".format(user))
        self.introLabel.config(text = "Signed in as {}".format(user))

    def toggleTheme(self, event = 0):
        self.theme *= -1 #Multiply theme number by -1, so 1 becomes -1 and -1 becomes 1
        colour = self.themeColours[self.theme] # this variable makes typing code easier
        self.config(bg = colour)
        self.phonebook.config(bg = colour)
        self.yscrollbar.config(bg = colour)

        self.rightFrame.config(bg = colour)
        self.dateLabel.config(bg = colour)
        self.introLabel.config(bg = colour)

        self.leftFrame.config(bg = colour)


    def close(self):
        if messagebox.askyesno("Quit?", "Quit program? Warning: If you haven't exported the results, your data will be gone."):
            if not self.addPrompt is None:
                self.addPrompt.destroy()

            if not self.editPrompt is None:
                self.editPrompt.destroy()

            if not self.exportWindow is None:
                self.exportWindow.destroy()

            if not self.docsWindow is None:
                self.docsWindow.destroy()

            self.destroy()
            exit()

#run
app = Window()
app.mainloop()
