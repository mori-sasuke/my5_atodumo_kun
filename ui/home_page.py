import tkinter as tk
from tkinter import ttk
from logic.constants import FONT

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller  

        title_label = ttk.Label(self, text="後ヅモ君 ホーム", font=FONT)
        title_label.pack(pady=20)

        # 推測ボタン
        guess_btn = ttk.Button(self, text="推測ページへ", command=self.controller.show_estimation)
        guess_btn.pack(pady=10)

        # 成績ボタン（後で実装予定）
        score_btn = ttk.Button(self, text="成績ページへ", command=self.controller.show_score)  # show_scoreが未実装ならあとで
        score_btn.pack(pady=10)

        # 終了ボタン
        exit_btn = ttk.Button(self, text="終了", command=self.controller.quit)
        exit_btn.pack(pady=10)
