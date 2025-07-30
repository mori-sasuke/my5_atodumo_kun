import tkinter as tk
from tkinter import ttk, messagebox
from logic.calculator import evaluate_all
from logic.constants import FONT

class EstimationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # タイトル
        title_label = ttk.Label(self, text="推測ページ", font=FONT)
        title_label.pack(pady=10)

        # 入力欄
        self.spin_var = tk.StringVar()
        self.big_var = tk.StringVar()
        self.reg_var = tk.StringVar()
        self.diff_var = tk.StringVar()

        self.create_entry_row("回転数", self.spin_var).pack(pady=5)
        self.create_entry_row("BIG回数", self.big_var).pack(pady=5)
        self.create_entry_row("REG回数", self.reg_var).pack(pady=5)
        self.create_entry_row("差枚数", self.diff_var).pack(pady=5)

        self.judge_btn = ttk.Button(self, text="判定", command=self.on_judge)
        self.judge_btn.pack(pady=10)

        # 正式参考値を表示
        reference_text = self.get_reference_text()
        self.reference_label = tk.Label(self, text=reference_text, font=("Courier", 10), justify="left", anchor="w")
        self.reference_label.pack(pady=10)

        self.result_text = tk.Text(self, width=60, height=10, state="disabled")
        self.result_text.pack(pady=10)

        reset_btn = ttk.Button(self, text="リセット", command=self.reset_fields)
        reset_btn.pack(pady=5)

        home_btn = ttk.Button(self, text="ホーム", command=controller.show_home)
        home_btn.pack(pady=5)

        self.spin_var.trace_add("write", self.update_judge_button)

    def create_entry_row(self, label_text, variable):
        frame = ttk.Frame(self)
        label = ttk.Label(frame, text=label_text, width=10)
        label.pack(side="left")
        entry = ttk.Entry(frame, textvariable=variable, width=10)
        entry.pack(side="left")
        return frame

    def update_judge_button(self, *_):
        try:
            spins = int(self.spin_var.get())
            self.judge_btn.state(["!disabled"] if spins >= 0 else ["disabled"])
        except ValueError:
            self.judge_btn.state(["disabled"])

    def on_judge(self):
        try:
            spins = int(self.spin_var.get().strip())
            big = int(self.big_var.get().strip())
            reg = int(self.reg_var.get().strip())
            diff = int(self.diff_var.get().strip())

            if spins < 3000:
                self.display_result("根拠が薄いです、今日は帰りましょう。")
                return

            results = evaluate_all(spins, big, reg, diff)

            # ブドウ確率を指定式で計算し上書き
            budo_prob = self.calculate_grape_probability(spins, big, reg, diff)
            if "ブドウ" in results:
                results["ブドウ"]["actual"] = budo_prob
            else:
                results["ブドウ"] = {"actual": budo_prob, "closest": None, "setting_value": None}

            self.display_result(self.format_result(results))

        except ValueError:
            messagebox.showerror("入力エラー", "全ての項目に正しい数値を入力してください。")

    def display_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")

    def reset_fields(self):
        self.spin_var.set("")
        self.big_var.set("")
        self.reg_var.set("")
        self.diff_var.set("")
        self.display_result("")

    def format_result(self, results):
        order = ["BIG", "REG", "合算", "ブドウ"]
        formatted = ""
        for key in order:
            if key in results:
                value = results[key]
                actual = value.get("actual")
                closest = value.get("closest")
                setting_val = value.get("setting_value")

                actual_str = f"1/{actual:.1f}" if actual else "N/A"
                setting_str = f"1/{setting_val:.1f}" if setting_val else "N/A"
                setting_num = f"設定{closest}" if closest else "設定不明"

                formatted += f"{key}：{actual_str} → {setting_num}（参考値：{setting_str}）\n"
            else:
                formatted += f"{key}：データなし\n"
        return formatted

    def get_reference_text(self):
        setting_data = {
            1: {"BIG": 273.1, "REG": 409.6, "合算": 163.8, "ブドウ": 5.90},
            2: {"BIG": 270.8, "REG": 385.5, "合算": 159.1, "ブドウ": 5.85},
            3: {"BIG": 266.4, "REG": 336.1, "合算": 148.6, "ブドウ": 5.80},
            4: {"BIG": 254.0, "REG": 290.0, "合算": 135.4, "ブドウ": 5.78},
            5: {"BIG": 240.1, "REG": 268.6, "合算": 126.8, "ブドウ": 5.76},
            6: {"BIG": 229.1, "REG": 229.1, "合算": 114.6, "ブドウ": 5.66},
        }

        text = "【設定別参考値】\n"
        for s, vals in setting_data.items():
            text += f"設定{s}：BIG 1/{vals['BIG']}　REG 1/{vals['REG']}　合算 1/{vals['合算']}　ブドウ 1/{vals['ブドウ']}\n"
        return text

    def calculate_grape_probability(self, spins, big, reg, diff):
        try:
            payout = (big * 239.25) + (reg * 95.25) + (spins * 0.411) + (spins * 0.04228)
            coin_in = spins * 3
            grape_base = ((diff - diff * 2) - (coin_in - payout)) / 8  # = (-diff - 差分)/8

            if grape_base == 0:
                return None  # ゼロ除算防止

            grape_part1 = spins / grape_base
            grape_part2 = (spins / grape_base) * 2

            grape_prob = grape_part1 - grape_part2
            return grape_prob
        except Exception as e:
            print(f"Error in calculate_grape_probability: {e}")
            return None





