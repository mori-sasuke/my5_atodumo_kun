import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
import tkinter as tk
from ui.home_page import HomePage
from ui.estimation_page import EstimationPage
from ui.result_page import ResultPage


class AtodumoKunApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("後ヅモ君")
        self.geometry("700x600")
        self.resizable(False, False)
        self.current_frame = None
        self.show_start_screen()

    def show_start_screen(self):
        if self.current_frame:
            self.current_frame.destroy()

        frame = tk.Frame(self)
        frame.pack(expand=True)

        label = tk.Label(frame, text="これはマイジャグラーV専用の設定推測器です\n過度な期待は禁物です。\nやめるなら今のうちですよ。", font=("Helvetica", 14), pady=20)
        label.pack()

        proceed_button = tk.Button(frame, text="進む", command=self.show_home)
        proceed_button.pack(pady=10)

        exit_button = tk.Button(frame, text="終了", command=self.quit)
        exit_button.pack()

        self.current_frame = frame

    def show_home(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = HomePage(self, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_estimation(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = EstimationPage(self, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_score(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ResultPage(self, self)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AtodumoKunApp()
    app.mainloop()
