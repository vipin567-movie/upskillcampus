"""
Project Title : Interactive Quiz Game with File Handling & Analytics
Domain        : Python Development
Intern Name   : Vipin Kumar
Program       : Industrial Internship — upskill Campus & The IoT Academy (UCT)
"""

import json
import os
from datetime import datetime
import numpy as np
import pandas as pd

QUESTION_BANK_FILE = "quiz_questions.json"
SCORE_HISTORY_FILE = "quiz_scores.csv"


def initialize_question_bank(filepath: str = QUESTION_BANK_FILE) -> list:
    """Create a default JSON question bank if one does not already exist."""
    default_questions = [
        {
            "id": 1,
            "category": "Python Basics",
            "question": "Which keyword is used to define a function in Python?",
            "options": ["A. func", "B. define", "C. def", "D. function"],
            "answer": "C",
        },
        {
            "id": 2,
            "category": "Data Structures",
            "question": "Which of the following Python data types is immutable?",
            "options": ["A. List", "B. Dictionary", "C. Set", "D. Tuple"],
            "answer": "D",
        },
        {
            "id": 3,
            "category": "File Handling",
            "question": "Which file mode opens a file for appending without truncating existing data?",
            "options": ["A. 'w'", "B. 'a'", "C. 'r+'", "D. 'x'"],
            "answer": "B",
        },
        {
            "id": 4,
            "category": "NumPy",
            "question": "Which NumPy function creates an array of evenly spaced values within a given interval?",
            "options": ["A. np.arange()", "B. np.empty()", "C. np.identity()", "D. np.ravel()"],
            "answer": "A",
        },
        {
            "id": 5,
            "category": "Pandas",
            "question": "What is the primary two-dimensional labeled data structure in Pandas?",
            "options": ["A. Series", "B. Panel", "C. DataFrame", "D. Ndarray"],
            "answer": "C",
        },
        {
            "id": 6,
            "category": "Control Flow",
            "question": "What does the 'break' statement do inside a Python loop?",
            "options": [
                "A. Skips the current iteration",
                "B. Terminates the loop immediately",
                "C. Restarts the loop from index 0",
                "D. Pauses execution for 1 second",
            ],
            "answer": "B",
        },
        {
            "id": 7,
            "category": "String Slicing",
            "question": "What is the output of 'Python'[::-1]?",
            "options": ["A. 'Python'", "B. 'nohtyP'", "C. 'P'", "D. Error"],
            "answer": "B",
        },
        {
            "id": 8,
            "category": "OOP & Scope",
            "question": "What does 'self' represent inside a Python class method?",
            "options": [
                "A. The parent module",
                "B. A global variable",
                "C. The current instance of the class",
                "D. A static constant",
            ],
            "answer": "C",
        },
    ]

    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(default_questions, file, indent=4)

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_choice(prompt: str = "Enter your answer (A/B/C/D): ") -> str:
    """Validate user input so only A, B, C, or D is accepted."""
    valid_options = {"A", "B", "C", "D"}
    while True:
        choice = input(prompt).strip().upper()
        if choice in valid_options:
            return choice
        print("Invalid choice. Please enter A, B, C, or D.")


def save_session_result(
    player_name: str,
    scores_array: np.ndarray,
    total_questions: int,
    filepath: str = SCORE_HISTORY_FILE,
) -> pd.DataFrame:
    """Compute NumPy metrics and append session results to a Pandas-managed CSV."""
    total_score = int(np.sum(scores_array))
    accuracy_pct = round(float(np.mean(scores_array) * 100), 2)

    record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Player_Name": player_name,
        "Score": total_score,
        "Total_Questions": total_questions,
        "Accuracy_Percent": accuracy_pct,
    }

    new_row = pd.DataFrame([record])
    if os.path.exists(filepath):
        history_df = pd.read_csv(filepath)
        updated_df = pd.concat([history_df, new_row], ignore_index=True)
    else:
        updated_df = new_row

    updated_df.to_csv(filepath, index=False)
    return updated_df


def display_analytics(filepath: str = SCORE_HISTORY_FILE) -> None:
    """Display summary statistics across recorded attempts using NumPy and Pandas."""
    if not os.path.exists(filepath):
        print("\nNo score history available yet. Play a round first!")
        return

    df = pd.read_csv(filepath)
    accuracies = df["Accuracy_Percent"].to_numpy(dtype=float)

    print("\n" + "=" * 56)
    print("QUIZ ANALYTICS & LEADERBOARD SUMMARY")
    print("=" * 56)
    print(df.tail(5).to_string(index=False))
    print("-" * 56)
    print(f"Total Attempts Recorded : {len(df)}")
    print(f"Mean Accuracy (NumPy)   : {np.mean(accuracies):.2f}%")
    print(f"Highest Accuracy        : {np.max(accuracies):.2f}%")
    print(f"Std Deviation           : {np.std(accuracies):.2f}%")
    print("=" * 56)


def run_quiz(player_name: str, questions: list) -> None:
    """Execute one full interactive quiz round and record per-question outcomes."""
    print(f"\nWelcome, {player_name}! Starting Quiz ({len(questions)} Questions)...\n")
    question_results = []

    for idx, item in enumerate(questions, start=1):
        print(f"Q{idx} [{item['category']}]: {item['question']}")
        for opt in item["options"]:
            print(f"   {opt}")

        user_ans = validate_choice()
        if user_ans == item["answer"]:
            print("   -> Correct!\n")
            question_results.append(1)
        else:
            print(f"   -> Incorrect! Correct answer: {item['answer']}\n")
            question_results.append(0)

    scores_np = np.array(question_results, dtype=int)
    total_score = int(np.sum(scores_np))
    accuracy = float(np.mean(scores_np) * 100)

    print("=" * 56)
    print(f"ROUND COMPLETE — {player_name}")
    print(f"Final Score : {total_score} / {len(questions)} ({accuracy:.2f}%)")
    print("=" * 56)

    save_session_result(player_name, scores_np, len(questions))


def main() -> None:
    """Main CLI menu loop for the Quiz Game application."""
    questions = initialize_question_bank()
    player_name = input("Enter your name: ").strip() or "Vipin Kumar"

    while True:
        print("\n--- PYTHON QUIZ GAME MENU ---")
        print("1. Start Quiz")
        print("2. View Performance Analytics (NumPy & Pandas)")
        print("3. Exit")
        selection = input("Select an option (1-3): ").strip()

        if selection == "1":
            run_quiz(player_name, questions)
        elif selection == "2":
            display_analytics()
        elif selection == "3":
            print("Thank you for playing! Exiting Quiz Game.")
            break
        else:
            print("Invalid selection. Choose 1, 2, or 3.")


if __name__ == "__main__":
    main()