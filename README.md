🐱 PURR$E — Mood-Based Expense Tracker
Ever noticed how your mood affects how much you spend? Sometimes when you passed a test, you buy things saying "Deserve ko man ini kay pasado ako".That is emotional spending in action. PURR$E is a small Flask web app that lets you log expenses alongside how you were feeling when you made them — whether you were happy, stressed, bored, or just hungry. Over time, you get a clearer picture of your spending habits and which emotions are doing the most damage to your wallet.

📌What It Does

-Log an expense with a description, your mood at the time, the amount, and a category
-Delete any entry you've added
-See your grand total, your top spending category, and the mood you spend the most in — all updated live
-Everything saves to a CSV file automatically, so nothing gets lost when you close the browser


Categories
😸🍜Food Category
😸💊Medical Category
😸🚐Transpo Category
😸🏠Utilities Category

📌OOP Concepts Applied

This project was built with clean Object-Oriented Programming in mind. Here's how each principle shows up in the code:
>Encapsulation — Internal data like expense lists and file paths are kept private using _variable naming. You interact with them through methods, not directly.

>Single Responsibility Principle — Every class has exactly one job. InputValidator validates. CostCalculator calculates. MoodAnalyzer analyzes moods. Nobody does more than they should.

>Open/Closed Principle — Adding a new spending category doesn't require touching any class logic. The CATEGORIES list at the top is all you need to change.

>Dependency Injection — MoodExpenseManager accepts an optional CSV_Data object on creation, making it easy to swap in a test file without touching the real data. This is what makes the unit tests work cleanly.

📌Tech Stack

- Python 3 — main language
- Flask — handles the web routes and form submissions
- CSV — lightweight file-based storage, no database needed
- HTML/CSS — rendered server-side as Python strings 


📌Project Structure
```
PurrseApp/
│
├── purrseapp.py
├── purrserecord.csv
│
└── tests/
    ├── test_CostCalculator.py
    ├── test_CSV_Data.py
    ├── test_InputValidator.py
    ├── test_Manage_Expense.py
    ├── test_MoodAnalyzer.py
    ├── test_MoodExpenseManager.py
    └── test_PageBuilder.py
```

📌How to Run It

Make sure you have Python installed, then:
1. Install Flask pip install flask
2. Start or run the app python purrseapp.py
3. Open your browser and go to
http://127.0.0.1:5000
That's it! 


📌A Few Things Worth Noting

- Descriptions and moods can't contain numbers — the validator will reject them
- Negative costs aren't allowed either


