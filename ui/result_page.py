import tkinter as tk
from tkinter import ttk, messagebox
from logic.constants import FONT
import os

SAVE_FILE = "total_score.txt"

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 通算収支をファイルから読み込む
        self.total_diff = self.load_total_diff()

        # タイトル
        title_label = ttk.Label(self, text="成績ページ", font=FONT)
        title_label.pack(pady=10)

        # 入力欄
        self.invest_var = tk.StringVar()
        self.payback_var = tk.StringVar()

        self.create_label_entry_row("投資枚数", self.invest_var).pack(pady=5)
        self.create_label_entry_row("回収枚数", self.payback_var).pack(pady=5)

        # 判定ボタン
        calc_btn = ttk.Button(self, text="判定", command=self.on_calculate)
        calc_btn.pack(pady=10)

        # 結果表示欄
        self.result_label = ttk.Label(self, text="", font=FONT)
        self.result_label.pack(pady=5)

        self.total_label = ttk.Label(self, text=f"通算収支: {self.total_diff} 枚", font=FONT)
        self.total_label.pack(pady=5)

        # リセットボタン（通算収支は消さない）
        reset_btn = ttk.Button(self, text="リセット", command=self.reset_fields)
        reset_btn.pack(pady=10)

        # ホームボタン
        home_btn = ttk.Button(self, text="ホーム", command=controller.show_home)
        home_btn.pack(pady=5)

    def create_label_entry_row(self, label_text, var):
        frame = ttk.Frame(self)
        label = ttk.Label(frame, text=label_text, font=FONT, width=10)
        entry = ttk.Entry(frame, textvariable=var, width=20)
        label.pack(side="left")
        entry.pack(side="left")
        return frame

    def on_calculate(self):
        try:
            invest = int(self.invest_var.get())
            payback = int(self.payback_var.get())
            diff = payback - invest
            self.total_diff += diff

            # 保存
            self.save_total_diff()

            self.result_label.config(text=f"今回の収支: {diff} 枚")
            self.total_label.config(text=f"通算収支: {self.total_diff} 枚")

        except ValueError:
            messagebox.showerror("入力エラー", "正しい数値を入力してください。")

    def reset_fields(self):
        self.invest_var.set("")
        self.payback_var.set("")
        self.result_label.config(text="")

    def load_total_diff(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0

    def save_total_diff(self):
        with open(SAVE_FILE, "w") as f:
            f.write(str(self.total_diff))
