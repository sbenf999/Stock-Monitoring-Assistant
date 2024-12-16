import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class superWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.bind("<Shift-q>", self.onClosing)
        self.bind("<Command-w>", self.onClosing)
        self.createcommand('tk::mac::Quit', self.onClosing)

    def onClosing(self, event=0):
        self.destroy()