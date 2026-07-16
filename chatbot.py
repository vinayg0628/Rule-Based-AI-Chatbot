from datetime import datetime
import random

print("==== Welcome to Rule-Based AI Chatbot ====")
print("Type 'help' to see available commands.")

while True:
    user = input("You: ").lower()

    # Greetings
    if user in ["hi", "hello", "hey"]:
        print("Bot: Hello! How can I help you?")

    # Basic Questions
    elif user == "how are you":
        print("Bot: I am doing great!")

    elif user == "what is your name":
        print("Bot: I am a Rule-Based AI Chatbot.")

    elif user == "who created you":
        print("Bot: I was created by Vinay.")

    elif user == "what can you do":
        print("Bot: I can answer simple questions, tell time, tell jokes, perform calculations, and more.")

    # Date and Time
    elif user == "time":
        print("Bot:", datetime.now().strftime("%H:%M:%S"))

    elif user in ["date", "today's date"]:
        print("Bot:", datetime.now().strftime("%d-%m-%Y"))

    elif user == "day":
        print("Bot:", datetime.now().strftime("%A"))

    elif user == "month":
        print("Bot:", datetime.now().strftime("%B"))

    # Joke
    elif user == "joke":
        print("Bot: Why do programmers prefer dark mode? Because light attracts bugs!")

    # Quote
    elif user == "quote":
        print("Bot: Success is the sum of small efforts repeated day after day.")

    # Fact
    elif user == "fact":
        print("Bot: Honey never spoils. Archaeologists have found edible honey thousands of years old!")

    # Motivation
    elif user == "motivate me":
        print("Bot: Believe in yourself! Every expert was once a beginner.")

    # Calculator
    elif user == "calculator":
        num1 = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if op == "+":
            print("Result:", num1 + num2)
        elif op == "-":
            print("Result:", num1 - num2)
        elif op == "*":
            print("Result:", num1 * num2)
        elif op == "/":
            if num2 != 0:
                print("Result:", num1 / num2)
            else:
                print("Cannot divide by zero.")
        else:
            print("Invalid operator.")

    # Square
    elif user == "square":
        num = float(input("Enter a number: "))
        print("Bot: Square =", num ** 2)

    # Even or Odd
    elif user == "even odd":
        num = int(input("Enter a number: "))
        if num % 2 == 0:
            print("Bot: It is an Even number.")
        else:
            print("Bot: It is an Odd number.")

    # Multiplication Table
    elif user == "table":
        num = int(input("Enter a number: "))
        print("Bot: Multiplication Table")
        for i in range(1, 11):
            print(f"{num} x {i} = {num * i}")

    # Dice Roll
    elif user == "dice":
        print("Bot: You rolled a", random.randint(1, 6))

    # Coin Toss
    elif user == "coin":
        print("Bot:", random.choice(["Heads", "Tails"]))

    # Help Menu
    elif user == "help":
        print("""
========== Available Commands ==========

Greetings
---------
hi
hello
hey

Basic Questions
---------------
how are you
what is your name
who created you
what can you do

Date & Time
-----------
time
date
today's date
day
month

Fun
---
joke
quote
fact
motivate me
dice
coin

Math
----
calculator
square
even odd
table

Other
-----
help
bye
exit
quit

========================================
""")

    # Exit
    elif user in ["bye", "exit", "quit"]:
        print("Bot: Goodbye! Have a nice day.")
        break

    # Unknown Command
    else:
        print("Bot: Sorry, I don't understand that. Type 'help' to see available commands.")