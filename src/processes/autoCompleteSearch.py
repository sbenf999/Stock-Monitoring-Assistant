import customtkinter as ctk
import tkinter as tk


class AutocompleteEntry(ctk.CTkEntry):
    def __init__(self, master=None, get_filter=None, **kwargs):
        super().__init__(master, **kwargs)

        self.get_filter = get_filter  
        self.suggestionsButtons = []
        self.suggestions = []
        self.allSuggestions = {}

        self.bind("<KeyRelease>", self.onKeyrelease)

    def onKeyrelease(self, event):
        typed = self.get().lower()
        current_filter = self.get_filter()() if self.get_filter else "All"

        if typed == "":
            self.hideSuggestions()
            return

        relevant_suggestions = self.allSuggestions.get(current_filter, self.allSuggestions.get("All", []))

        self.suggestions = [s for s in relevant_suggestions if typed in s.lower()]

        if self.suggestions:
            self.showSuggestions()

        else:
            self.hideSuggestions()

    def getEntryData(self):
        return self.get()

    def showSuggestions(self):
        self.hideSuggestions() 

        for i, suggestion in enumerate(self.suggestions):
            button = ctk.CTkButton(self.master, text=suggestion, command=lambda s=suggestion: self.onSuggestionClick(s), width=self.winfo_width())
            button.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height() + (i * 30), anchor="nw")

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
        """
        Accepts either:
        - A list: ["Apple", "Banana"]
        - A dict: {"Fruits": [...], "Vegetables": [...], "All": [...]}
        """
        if isinstance(suggestions, dict):
            self.allSuggestions = suggestions

        elif isinstance(suggestions, list):
            self.allSuggestions = {"All": suggestions}

        else:
            raise ValueError("Suggestions must be a list or dictionary.")
