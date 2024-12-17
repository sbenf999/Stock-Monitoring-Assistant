import customtkinter as ctk
import tkinter as tk

class AutocompleteEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.suggestions_listbox = None
        self.suggestions = []
        self.all_suggestions = []
        self.bind("<KeyRelease>", self.on_keyrelease)

    def on_keyrelease(self, event):
        #trigger autocomplete on key release
        typed = self.get().lower()
        if typed == "":
            if self.suggestions_listbox:
                self.suggestions_listbox.destroy()
                self.suggestions_listbox = None
            return

        # Filter suggestions based on the typed text
        self.suggestions = [s for s in self.all_suggestions if typed in s.lower()]
        
        if self.suggestions:
            if not self.suggestions_listbox:
                self.suggestions_listbox = tk.Listbox(self.master, height=5)
                self.suggestions_listbox.place(relx=0.5, rely=0.1, anchor="n")

            # Clear previous suggestions
            self.suggestions_listbox.delete(0, tk.END)
            
            # Insert the new matching suggestions
            for suggestion in self.suggestions:
                self.suggestions_listbox.insert(tk.END, suggestion)
            
            self.suggestions_listbox.bind("<ButtonRelease-1>", self.on_suggestion_click)
        else:
            if self.suggestions_listbox:
                self.suggestions_listbox.destroy()
                self.suggestions_listbox = None

    def on_suggestion_click(self, event):
        #andle clicking a suggestion from the listbox
        selected = self.suggestions_listbox.get(self.suggestions_listbox.curselection())
        self.delete(0, tk.END)
        self.insert(0, selected)
        self.suggestions_listbox.destroy()
        self.suggestions_listbox = None

    def set_suggestions(self, suggestions):
        #Set the complete list of suggestions for autocomplete"""
        self.all_suggestions = suggestions


