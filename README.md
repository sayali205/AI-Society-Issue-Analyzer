# 🤖 AI-Based Society Issue Analyzer

AI-Based Society Issue Analyzer is a Machine Learning web application that analyzes society complaints and predicts their priority level (High, Medium, Low).

## 🚀 Features

- User Registration and Login
- Complaint submission system
- AI priority prediction using Machine Learning
- Admin dashboard
- Complaint history
- SQLite database integration

## 🧠 Technologies Used

- Python
- Flask
- Machine Learning (Scikit-learn)
- HTML, CSS
- SQLite
- Joblib

## 📂 Project Structure

AI-Society-Issue-Analyzer/
│
├── app.py
├── complaint_model.pkl
├── society.db
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ └── dashboard.html
│
└── README.md


## ▶️ How to Run

▶️ How to Run
Step 1: Install Python

Download and install Python from:
https://www.python.org/downloads/

Make sure to check ✔ Add Python to PATH

Verify installation:

python --version

Step 2: Install Required Libraries

Open Command Prompt in your project folder and run:

pip install flask
pip install scikit-learn
pip install joblib


OR install all together:

pip install flask scikit-learn joblib

Step 3: Download or Clone Project

Option 1: Download ZIP from GitHub

Option 2: Clone using command:

git clone https://github.com/sayali205/AI-Society-Issue-Analyzer.git

Step 4: Open Project Folder
cd AI-Society-Issue-Analyzer

Step 5: Run the Application
python app.py

Step 6: Open in Browser

Open this link:

http://127.0.0.1:5000

Step 7: Register and Login

• Click Register
• Create account
• Login
• Submit complaint
• View AI prediction

👤 Default Admin Login (Optional)

Username:

admin


Password:

admin123

📊 Example Complaint

Input:

Water not coming since morning


Output:

Priority: High
Recommended Action: Notify society secretary immediately

