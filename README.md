# Enhanced Rule-Based AI Chatbot

A comprehensive Python-based chatbot suite offering a modern rule-based assistant across three distinct interfaces: a **polished Flask-based Web Interface** with multi-session chat tracking, a **Tkinter Desktop App**, and a **Command Line Interface (CLI)**.

---

## 🚀 Key Features

* **Multi-Session Chat Support (Web)**:
  * Create new distinct chat threads.
  * Auto-generation of chat titles based on the first user message.
  * Dynamically switch between conversations and view historical messages.
  * Delete individual chat sessions.
* **Persistent SQLite Storage (Web)**: Saves chats and messages locally. Includes automatic schema migrations for legacy databases.
* **Rule-Based Intellect**:
  * **Greetings & Q&A**: Answers basic questions, greetings, and custom queries.
  * **Date & Time**: Displays current time, date, day of the week, and month.
  * **Fun & Leisure**: Tells programmer jokes, delivers motivational quotes, and reveals interesting facts.
  * **Math Assistants**: Built-in calculator, square calculator, even/odd checker, and multiplication table generator.
  * **Random Games**: Mini dice roll and coin toss simulation.
  * **Help Menu**: Detailed list of commands available to the user.

---

## 📁 Project Structure

```text
├── app_server.py       # Main entry point to run the Flask Web Application
├── backend.py           # Flask app configurations, SQLite DB logic, & chatbot responses
├── app.py               # Tkinter GUI-based Desktop Application
├── chatbot.py           # Continuous interactive Command-Line Interface (CLI)
├── chatbot.db           # SQLite database storing Web chat logs (Auto-created)
├── templates/
│   └── index.html       # Modern responsive web layout (Glassmorphism & dark-mode sidebar)
├── requirements.txt     # Python packages for Web deployment
├── .gitignore           # Excludes virtual environments, pycaches, and DB files
└── README.md            # You are here!
```

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.x** installed.

1. **Clone or Navigate to the Directory**:
   ```bash
   cd RuleBasedChatbot
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**:
   * **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD)**:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   * **macOS / Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 How to Run

You can choose to run any of the three versions of the chatbot:

### 1. Web Application (Recommended)
Runs a modern browser-based interface complete with multi-chat side panel.
```bash
python app_server.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

### 2. Desktop GUI App
Launches a standalone Tkinter desktop application window.
```bash
python app.py
```

### 3. CLI Chatbot
Runs directly in your terminal/command line interface.
```bash
python chatbot.py
```

---

## 📋 Available Chatbot Commands

Below is the list of commands recognized by the chatbot across the interfaces:

| Command Category | Commands |
| :--- | :--- |
| **Greetings** | `hi`, `hello`, `hey` |
| **Information** | `how are you`, `what is your name`, `who created you`, `what can you do` |
| **Temporal** | `time`, `date`, `today's date`, `day`, `month` |
| **Fun & Games** | `joke`, `quote`, `fact`, `motivate me`, `dice`, `coin` |
| **Mathematics** | `calculator`, `square`, `even odd`, `table` |
| **System** | `help`, `bye`, `exit`, `quit` |

---

## 💾 Database Schema

The Web application uses SQLite (`chatbot.db`) configured with two related tables to manage different chats:

#### 1. `chats` Table
* `id` (INTEGER, Primary Key)
* `title` (TEXT)
* `created_at` (TEXT)

#### 2. `chat_messages` Table
* `id` (INTEGER, Primary Key)
* `chat_id` (INTEGER, Foreign Key referencing `chats(id)`)
* `sender` (TEXT - `user` or `bot`)
* `message` (TEXT)
* `created_at` (TEXT)
