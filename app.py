import random
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, scrolledtext


class RuleBasedChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rule-Based AI Chatbot")
        self.root.geometry("760x620")
        self.root.resizable(False, False)

        self.create_widgets()
        self.add_message("Bot", "Hello! Type 'help' to see available commands.")

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="Rule-Based AI Chatbot",
            font=("Segoe UI", 16, "bold"),
            padx=10,
            pady=10,
        )
        title_label.pack(fill=tk.X)

        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            state="disabled",
            padx=10,
            pady=10,
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.entry = tk.Entry(bottom_frame, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        send_button = tk.Button(bottom_frame, text="Send", width=12, command=self.send_message)
        send_button.pack(side=tk.LEFT, padx=(10, 0))

        self.entry.focus_set()

    def add_message(self, sender, message):
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.yview(tk.END)

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return

        self.entry.delete(0, tk.END)
        self.add_message("You", text)
        response = self.get_response(text)
        self.add_message("Bot", response)

    def get_response(self, user_input):
        user_input = user_input.lower().strip()

        if user_input in ["hi", "hello", "hey"]:
            return "Hello! How can I help you?"
        elif user_input == "how are you":
            return "I am doing great!"
        elif user_input == "what is your name":
            return "I am a Rule-Based AI Chatbot."
        elif user_input == "who created you":
            return "I was created by Vinay."
        elif user_input == "what can you do":
            return "I can answer simple questions, tell time, tell jokes, perform calculations, and more."
        elif user_input == "time":
            return datetime.now().strftime("%H:%M:%S")
        elif user_input in ["date", "today's date"]:
            return datetime.now().strftime("%d-%m-%Y")
        elif user_input == "day":
            return datetime.now().strftime("%A")
        elif user_input == "month":
            return datetime.now().strftime("%B")
        elif user_input == "joke":
            return "Why do programmers prefer dark mode? Because light attracts bugs!"
        elif user_input == "quote":
            return "Success is the sum of small efforts repeated day after day."
        elif user_input == "fact":
            return "Honey never spoils. Archaeologists have found edible honey thousands of years old!"
        elif user_input == "motivate me":
            return "Believe in yourself! Every expert was once a beginner."
        elif user_input == "calculator":
            try:
                num1 = simpledialog.askfloat("Calculator", "Enter first number:")
                if num1 is None:
                    return "Calculator canceled."
                op = simpledialog.askstring("Calculator", "Enter operator (+, -, *, /):")
                if op is None:
                    return "Calculator canceled."
                num2 = simpledialog.askfloat("Calculator", "Enter second number:")
                if num2 is None:
                    return "Calculator canceled."

                if op == "+":
                    return f"Result: {num1 + num2}"
                elif op == "-":
                    return f"Result: {num1 - num2}"
                elif op == "*":
                    return f"Result: {num1 * num2}"
                elif op == "/":
                    if num2 != 0:
                        return f"Result: {num1 / num2}"
                    return "Cannot divide by zero."
                return "Invalid operator."
            except Exception:
                return "Invalid input. Please enter numeric values."
        elif user_input == "square":
            try:
                num = simpledialog.askfloat("Square", "Enter a number:")
                if num is None:
                    return "Operation canceled."
                return f"Square = {num ** 2}"
            except Exception:
                return "Invalid input."
        elif user_input == "even odd":
            try:
                num = simpledialog.askinteger("Even or Odd", "Enter a number:")
                if num is None:
                    return "Operation canceled."
                if num % 2 == 0:
                    return "It is an Even number."
                return "It is an Odd number."
            except Exception:
                return "Invalid input."
        elif user_input == "table":
            try:
                num = simpledialog.askinteger("Multiplication Table", "Enter a number:")
                if num is None:
                    return "Operation canceled."
                lines = [f"{num} x {i} = {num * i}" for i in range(1, 11)]
                return "\n".join(lines)
            except Exception:
                return "Invalid input."
        elif user_input == "dice":
            return f"You rolled a {random.randint(1, 6)}"
        elif user_input == "coin":
            return random.choice(["Heads", "Tails"])
        elif user_input == "help":
            return (
                "Available commands:\n"
                "hi, hello, hey\n"
                "how are you\n"
                "what is your name\n"
                "who created you\n"
                "what can you do\n"
                "time\n"
                "date\n"
                "today's date\n"
                "day\n"
                "month\n"
                "joke\n"
                "quote\n"
                "fact\n"
                "motivate me\n"
                "calculator\n"
                "square\n"
                "even odd\n"
                "table\n"
                "dice\n"
                "coin\n"
                "help\n"
                "bye, exit, quit"
            )
        elif user_input in ["bye", "exit", "quit"]:
            return "Goodbye! Have a nice day."
        else:
            return "Sorry, I don't understand that. Type 'help' to see available commands."


if __name__ == "__main__":
    root = tk.Tk()
    app = RuleBasedChatbotApp(root)
    root.mainloop()
