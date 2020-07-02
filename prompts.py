from tkinter import Tk, Label, Entry, Frame, Button, StringVar, Text, messagebox, filedialog, NORMAL, DISABLED, BOTTOM, END
import pathlib

class AddPerson(Tk):
    def __init__(self, master):
        Tk.__init__(self)
        self.master = master
        self.title("+")
        self.resizable(height=False, width=False)

        self.entriesFrame = Frame(self)

        self.nameLabel = Label(self.entriesFrame, text="Name: ")
        self.numberLabel = Label(self.entriesFrame, text="Number: ")

        self.nameEntry = Entry(self.entriesFrame)
        self.numberEntry = Entry(self.entriesFrame)

        self.confirmButton = Button(self, text = "Add", command = self.add)

        self.entriesFrame.pack()
        self.confirmButton.pack()
        self.nameLabel.grid(row=0, column=0)
        self.numberLabel.grid(row=1, column=0)
        self.nameEntry.grid(row=0, column=1)
        self.numberEntry.grid(row=1, column=1)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        self.master.addPrompt.destroy()
        self.master.addPrompt = None

    def add(self):
        if self.nameEntry.get() == "" or self.numberEntry.get() == "":
            messagebox.showerror("Invalid entries", "Please enter something in both fields.")

        else:
            self.master.phonebook.insert(END, "{}: {}".format(self.nameEntry.get(), self.numberEntry.get()))
            self.master.phonebook_list.append("{}: {}".format(self.nameEntry.get(), self.numberEntry.get()))
            self.close()


class EditPerson(Tk): #Bug
    def __init__(self, master):
        Tk.__init__(self)
        self.master = master
        self.title("Edit")
        self.resizable(height = False, width = False)

        self.editFrame = Frame(self)

        self.nameLabel = Label(self.editFrame, text = "Name: ")
        self.numberLabel = Label(self.editFrame, text = "Number: ")
        self.nameEntry = Entry(self.editFrame)
        self.numberEntry = Entry(self.editFrame)

        self.confirmButton = Button(self, text = "Edit", command = self.edit)

        self.editFrame.pack()
        self.nameLabel.grid(row=0,column=0)
        self.numberLabel.grid(row=1,column=0)
        self.nameEntry.grid(row=0,column=1)
        self.numberEntry.grid(row=1,column=1)
        self.confirmButton.pack()

        self.curselectionTemp = self.master.phonebook.curselection()[0]
        self.nameEntry.insert(0, self.master.phonebook_list[self.master.phonebook.curselection()[0]].split(":")[0])
        self.numberEntry.insert(0, self.master.phonebook_list[self.master.phonebook.curselection()[0]].split(":")[1][1:])
        self.protocol("WM_DELETE_WINDOW", self.close)

    def edit(self):
        self.master.phonebook.delete(self.curselectionTemp)
        self.master.phonebook_list.remove(self.master.phonebook_list[self.curselectionTemp])

        self.master.phonebook.insert(self.curselectionTemp, "{}: {}".format(self.nameEntry.get(), self.numberEntry.get()))
        self.master.phonebook_list.insert(self.curselectionTemp, "{}: {}".format(self.nameEntry.get(), self.numberEntry.get()))

        self.close()

    def close(self):
        self.master.editPrompt = None
        self.destroy()


class ExportWindow(Tk):
    def __init__(self, master):
        Tk.__init__(self)
        self.title("Export")
        self.master = master

        self.resizable(height=False, width=False)

        self.entriesFrame = Frame(self)

        self.usernameLabel = Label(self.entriesFrame, text = "Username: ")
        self.usernameEntry = Entry(self.entriesFrame)

        self.confirmButton = Button(self, text = "Export", command = self.exp)

        self.entriesFrame.pack()

        self.confirmButton.pack()
        self.usernameLabel.grid(row=0, column=0)
        self.usernameEntry.grid(row=0, column = 1)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def exp(self):
        self.master.update_user(self.usernameEntry.get())
        path = filedialog.asksaveasfilename(filetypes = (("Text file", "*.txt"), ("All files", "*.*")))

        file = open(path, "w")
        file.write("{}\nPhone numbers:\n".format(self.master.user))

        for i in self.master.phonebook.get(0, END):
            file.write(i+"\n")

        file.write("Phonebook 2")
        file.close()

        self.close()

    def close(self):
        self.master.exportWindow.destroy()
        self.master.exportWindow = None

class DocsWindow(Tk):
    def __init__(self, master):
        Tk.__init__(self)
        self.master = master
        self.title("Phonebook 2 Docs")
        self.resizable(width = False, height = False)
        self.page = 1
        self.maxPages = 4

        self.mainFrame = Frame(self)
        self.mainFrame.pack()

        self.introText = Label(self.mainFrame, text = "View the docs of Phonebook 2 here:")
        self.introText.pack()

        self.docsText = Text(self.mainFrame, width = 80, height = 20)
        self.docsText.pack()
        self.docsText.insert(END, open("{}/docs/page1.txt".format(pathlib.Path(__file__).parent.absolute()), "r").read())
        self.docsText.config(state = DISABLED)

        self.buttonsFrame = Frame(self)
        self.buttonsFrame.pack(side = BOTTOM)

        self.prevButton = Button(self.buttonsFrame, text = "Previous", command = self.prev)
        self.prevButton.grid(row=0,column=0)

        self.nextButton = Button(self.buttonsFrame, text = "Next", command = self.next)
        self.nextButton.grid(row=0,column=1)

        self.pagesLabel = Label(self.buttonsFrame, text = "Page 1 of 4")
        self.pagesLabel.grid(row=0,column=2)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def prev(self):
        if self.page == 1:
            self.page = self.maxPages
        
        else:
            self.page -= 1
        
        self.pagesLabel.config(text = "Page {} of {}".format(self.page, self.maxPages))
        self.docsText.config(state = NORMAL)
        self.docsText.delete(1.0, END)
        self.docsText.insert(END, open("{}/docs/page{}.txt".format(pathlib.Path(__file__).parent.absolute(), self.page), "r").read())
        self.docsText.config(state = DISABLED)

    def next(self):
        if self.page == self.maxPages:
            self.page = 1

        else:
            self.page +=1

        self.pagesLabel.config(text = "Page {} of {}".format(self.page, self.maxPages))
        self.docsText.config(state = NORMAL)
        self.docsText.delete(1.0, END)
        self.docsText.insert(END, open("{}/docs/page{}.txt".format(pathlib.Path(__file__).parent.absolute(), self.page), "r").read())
        self.docsText.config(state = DISABLED)

    def close(self):
        self.master.docsWindow = None
        self.destroy()