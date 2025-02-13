import customtkinter as ctk
import tkinter as tk

class AutocompleteEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.suggestionsButtons = []  #list to store the suggestion buttons
        self.suggestions = []
        self.allSuggestions = []
        self.bind("<KeyRelease>", self.onKeyrelease)

    def onKeyrelease(self, event):
        typed = self.get().lower()
        if typed == "":
            self.hideSuggestions()
            return

        self.suggestions = [s for s in self.allSuggestions if typed in s.lower()]
        
        if self.suggestions:
            self.showSuggestions()

        else:
            self.hideSuggestions()

    def getEntryData(self):
        return self.get()

    def showSuggestions(self):
        self.hideSuggestions()

        for i, suggestion in enumerate(self.suggestions):
            button = ctk.CTkButton(self.master, text=suggestion, command=lambda s=suggestion: self.onSuggestionClick(s))
            button.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height() + (i * 30), anchor="w")
            self.suggestionsButtons.append(button)

    def hideSuggestions(self):
        for button in self.suggestionsButtons:
            button.destroy()
        self.suggestionsButtons.clear()

    def onSuggestionClick(self, suggestion):
        self.delete(0, tk.END)
        self.insert(0, suggestion)
        self.hideSuggestions()

    def setSuggestions(self, suggestions):
        self.allSuggestions = suggestions
