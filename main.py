#!/usr/bin/env python3
# Простой калькулятор на Tkinter — Calculator_Project
# Рекомендуется запускать под Python 3.11

import tkinter as tk
from tkinter import font

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Простой Калькулятор")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        self._make_styles()
        self._create_widgets()
        self._place_buttons()
        self._reset_state()

    def _make_styles(self):
        self.display_font = font.Font(family="Arial", size=28)
        self.button_font = font.Font(family="Arial", size=16, weight="bold")
        self.color_digit = "#dedede"
        self.color_op = "#e74c3c"
        self.color_equal = "#2ecc71"

    def _create_widgets(self):
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(self, textvariable=self.display_var,
                                font=self.display_font, bd=3, relief="solid",
                                justify="right", bg="white", width=14)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 6))

    def _place_buttons(self):
        btn_cfg = {"font": self.button_font, "width": 5, "height": 2, "bd": 2}

        buttons = [
            ("7", 1, 0, self._on_digit, self.color_digit),
            ("8", 1, 1, self._on_digit, self.color_digit),
            ("9", 1, 2, self._on_digit, self.color_digit),
            ("/", 1, 3, lambda t="/": self._on_op(t), self.color_op),

            ("4", 2, 0, self._on_digit, self.color_digit),
            ("5", 2, 1, self._on_digit, self.color_digit),
            ("6", 2, 2, self._on_digit, self.color_digit),
            ("*", 2, 3, lambda t="*": self._on_op(t), self.color_op),

            ("1", 3, 0, self._on_digit, self.color_digit),
            ("2", 3, 1, self._on_digit, self.color_digit),
            ("3", 3, 2, self._on_digit, self.color_digit),
            ("-", 3, 3, lambda t="-": self._on_op(t), self.color_op),

            ("0", 4, 0, self._on_digit, self.color_digit),
            (".", 4, 1, self._on_dot, self.color_digit),
            ("=", 4, 2, self._on_equal, self.color_equal),
            ("+", 4, 3, lambda t="+": self._on_op(t), self.color_equal),

            ("C", 5, 0, self._on_clear, self.color_op),
            ("←", 5, 1, self._on_backspace, self.color_op),
        ]

        for (text, r, c, cmd, color) in buttons:
            btn = tk.Button(self, text=text, command=(lambda t=text, f=cmd: f(t)),
                            bg=color, activebackground=color, fg="black", **btn_cfg)
            if text == "C":
                btn.grid(row=r, column=c, columnspan=2, padx=8, pady=8, sticky="we")
            elif text == "←":
                btn.grid(row=r, column=c+1, columnspan=2, padx=8, pady=8, sticky="we")
            else:
                btn.grid(row=r, column=c, padx=8, pady=8)

        self.bind("<Key>", self._on_key)

    def _reset_state(self):
        self.current = ""
        self.left = None
        self.op = None

    def _on_digit(self, ch):
        if self.display_var.get() == "0" and ch != ".":
            self.display_var.set(ch)
        else:
            self.display_var.set(self.display_var.get() + ch)

    def _on_dot(self, ch):
        if "." not in self.display_var.get():
            self.display_var.set(self.display_var.get() + ".")

    def _on_op(self, operator):
        try:
            self.left = float(self.display_var.get())
        except Exception:
            self.left = 0.0
        self.op = operator
        self.display_var.set("0")

    def _on_equal(self, ch=None):
        try:
            right = float(self.display_var.get())
        except Exception:
            right = 0.0

        result = None
        try:
            if self.op == "+":
                result = self.left + right
            elif self.op == "-":
                result = self.left - right
            elif self.op == "*":
                result = self.left * right
            elif self.op == "/":
                if right == 0:
                    result = "Error"
                else:
                    result = self.left / right
            else:
                result = right
        except Exception:
            result = "Error"

        if isinstance(result, float):
            if result.is_integer():
                result = str(int(result))
            else:
                result = str(round(result, 10)).rstrip("0").rstrip(".")
        else:
            result = str(result)

        self.display_var.set(result)
        self.left = None
        self.op = None

    def _on_clear(self, ch=None):
        self.display_var.set("0")
        self._reset_state()

    def _on_backspace(self, ch=None):
        s = self.display_var.get()
        if len(s) <= 1:
            self.display_var.set("0")
        else:
            self.display_var.set(s[:-1])

    def _on_key(self, event):
        key = event.char
        if key.isdigit():
            self._on_digit(key)
        elif key == ".":
            self._on_dot(key)
        elif key in "+-*/":
            self._on_op(key)
        elif key == "\r":
            self._on_equal()
        elif key == "\x08":
            self._on_backspace()
        elif key.lower() == "c":
            self._on_clear()

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()