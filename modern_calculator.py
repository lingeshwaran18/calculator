import tkinter as tk

class ModernCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Calculator - with History")
        # Increase width to accommodate history panel
        self.geometry("640x480")
        self.resizable(False, False)
        self.configure(bg="#2E2E2E")
        
        self.expression = ""
        
        # Main layout: Left for calculator, Right for history
        calc_frame = tk.Frame(self, bg="#2E2E2E")
        calc_frame.pack(side="left", fill="both", expand=True)
        
        history_frame = tk.Frame(self, bg="#1E1E1E", width=250)
        history_frame.pack(side="right", fill="both")
        history_frame.pack_propagate(False) # Keep width fixed
        
        # --- History Setup ---
        tk.Label(
            history_frame, 
            text="History", 
            bg="#1E1E1E", 
            fg="#FFFFFF", 
            font=("Segoe UI", 16, "bold"), 
            pady=10
        ).pack(fill="x")
        
        self.history_list = tk.Listbox(
            history_frame, 
            bg="#1E1E1E", 
            fg="#AAAAAA", 
            font=("Segoe UI", 12), 
            borderwidth=0, 
            highlightthickness=0,
            selectbackground="#333333"
        )
        self.history_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        clear_history_btn = tk.Button(
            history_frame, 
            text="Clear History", 
            bg="#434343", 
            fg="#FFFFFF",
            font=("Segoe UI", 10),
            borderwidth=0,
            activebackground="#555555",
            activeforeground="#FFFFFF",
            command=self.clear_history
        )
        clear_history_btn.pack(fill="x", padx=10, pady=10)

        # --- Calculator Display ---
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(calc_frame, bg="#2E2E2E")
        display_frame.pack(fill="both")
        
        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            anchor="e", 
            bg="#2E2E2E", 
            fg="#FFFFFF", 
            font=("Segoe UI", 36, "bold"),
            padx=20,
            pady=20,
            height=2
        )
        display_label.pack(expand=True, fill="both")
        
        # --- Calculator Buttons ---
        buttons_frame = tk.Frame(calc_frame, bg="#1E1E1E")
        buttons_frame.pack(expand=True, fill="both")
        
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]
        
        for i in range(1, 6):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)
            
        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            colspan = button[3] if len(button) > 3 else 1
            
            button_color = "#434343"
            text_color = "#FFFFFF"
            active_bg = "#666666"
            
            if text in ['/', '*', '-', '+', '=']:
                button_color = "#FF9F0A"
                active_bg = "#FFB340"
            elif text in ['C', '±', '%']:
                button_color = "#A5A5A5"
                text_color = "#000000"
                active_bg = "#D4D4D4"
                
            btn = tk.Button(
                buttons_frame, 
                text=text, 
                bg=button_color, 
                fg=text_color, 
                font=("Segoe UI", 18), 
                borderwidth=0,
                activebackground=active_bg,
                activeforeground=text_color,
                highlightthickness=0,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display_var.set("0")
        elif char == '=':
            try:
                exp = self.expression.replace('%', '/100')
                result = str(eval(exp))
                if result.endswith('.0'):
                    result = result[:-2]
                
                # Add calculation to history panel
                if self.expression != "":
                    history_entry = f"{self.expression} = {result}"
                    self.history_list.insert(tk.END, history_entry)
                    self.history_list.yview(tk.END) # Scroll to the latest entry
                
                self.display_var.set(result)
                self.expression = result
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
        elif char == '±':
            try:
                if self.expression:
                    if self.expression.startswith('-'):
                        self.expression = self.expression[1:]
                    else:
                        self.expression = '-' + self.expression
                    self.display_var.set(self.expression)
            except Exception:
                pass
        else:
            if self.expression == "0" and char not in ['.', '/', '*', '+', '-']:
                self.expression = ""
            self.expression += str(char)
            self.display_var.set(self.expression)
            
    def clear_history(self):
        self.history_list.delete(0, tk.END)

if __name__ == "__main__":
    app = ModernCalculator()
    app.mainloop()
