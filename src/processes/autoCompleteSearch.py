import customtkinter as ctk
import tkinter as tk

class AutocompleteEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.suggestions_buttons = []  # A list to store the suggestion buttons
        self.suggestions = []
        self.all_suggestions = []
        self.bind("<KeyRelease>", self.on_keyrelease)

    def on_keyrelease(self, event):
        typed = self.get().lower()

        # If there's no text or if the typed text is empty, hide the suggestions
        if typed == "":
            self.hide_suggestions()
            return

        # Filter suggestions based on the typed text
        self.suggestions = [s for s in self.all_suggestions if typed in s.lower()]
        
        # Show suggestions if any are found
        if self.suggestions:
            self.show_suggestions()
        else:
            self.hide_suggestions()

    def show_suggestions(self):
        # Clear previous suggestion buttons
        self.hide_suggestions()
        
        # Create a button for each suggestion
        for i, suggestion in enumerate(self.suggestions):
            button = ctk.CTkButton(self.master, text=suggestion, command=lambda s=suggestion: self.on_suggestion_click(s))
            button.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height() + (i * 30), anchor="w")
            self.suggestions_buttons.append(button)

    def hide_suggestions(self):
        # Hide the suggestion buttons by destroying them
        for button in self.suggestions_buttons:
            button.destroy()
        self.suggestions_buttons.clear()

    def on_suggestion_click(self, suggestion):
        # Insert the clicked suggestion into the entry and hide suggestions
        self.delete(0, tk.END)
        self.insert(0, suggestion)
        self.hide_suggestions()

    def set_suggestions(self, suggestions):
        # Set the complete list of suggestions for autocomplete
        self.all_suggestions = suggestions
