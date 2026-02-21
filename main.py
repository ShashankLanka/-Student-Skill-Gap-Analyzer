import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# Skill Rating Guide
# -----------------------------
def print_skill_guide():
    print("\nSkill Rating Guide:")
    print("1 - Very Basic Knowledge")
    print("2 - Basic Understanding")
    print("3 - Intermediate Level")
    print("4 - Strong Knowledge")
    print("5 - Advanced / Expert Level")


# -----------------------------
# Safe Skill Input
# -----------------------------
def safe_skill_input(skill_name):
    while True:
        try:
            value = int(input(f"{skill_name} (1-5): "))
            if 1 <= value <= 5:
                return value
            else:
                print("Please enter a value between 1 and 5.")
        except:
            print("Invalid input. Enter numbers only.")


# -----------------------------
# Load Companies
# -----------------------------
def load_companies():
    while True:
        branch = input("\nEnter your branch (CSE/EEE/ECE/MECH) or 'back': ").strip().upper()

        if branch == "BACK":
            return None

        if branch == "CSE":
            return pd.read_csv("CSE_companies.csv")
        elif branch == "EEE":
            return pd.read_csv("EEE_companies.csv")
        elif branch == "ECE":
            return pd.read_csv("ECE_companies.csv")
        elif branch == "MECH":
            return pd.read_csv("MECH_companies.csv")
        else:
            print("Invalid branch. Try again.")


# -----------------------------
# Individual Mode
# -----------------------------
def individual_mode():

    companies = load_companies()
    if companies is None:
        return

    skills = companies.columns[1:]

    print_skill_guide()

    student_skills = {}
    print("\nEnter your skill levels:")
    for skill in skills:
        student_skills[skill] = safe_skill_input(skill)

    student_vector = np.array(list(student_skills.values()))
    results = {}

    # Alignment Calculation
    for index, row in companies.iterrows():
        company_name = row["Company"]
        company_vector = np.array(row[1:])

        score = np.dot(student_vector, company_vector)
        max_score = np.dot(np.ones(len(student_vector)) * 5, company_vector)

        alignment = (score / max_score) * 100 if max_score != 0 else 0
        results[company_name] = round(alignment, 2)

    sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    print("\nAlignment Results:")
    for company, percent in sorted_results.items():
        print(f"{company} → {percent}%")

    print("\nAvailable Companies:")
    for company in companies["Company"]:
        print("-", company)

    while True:
        selected_company = input("\nEnter company name for detailed analysis or 'back': ")

        if selected_company.lower() == "back":
            return

        if selected_company not in companies["Company"].values:
            print("Invalid company name. Try again.")
            continue

        selected_row = companies[companies["Company"] == selected_company].iloc[0]

        print(f"\nDetailed Skill Analysis for {selected_company}:")

        high_priority = []
        medium_priority = []

        for skill in skills:
            company_requirement = selected_row[skill]
            student_level = student_skills[skill]
            gap = company_requirement - student_level

            if gap > 0:
                status = f"Need +{gap} level(s)"
            elif gap == 0:
                status = "Perfect Match"
            else:
                status = "Exceeds Requirement"

            print(f"{skill} → Required: {company_requirement}, "
                  f"Your Level: {student_level}, Status: {status}")

            if company_requirement >= 4 and student_level <= 3:
                high_priority.append(skill)
            elif company_requirement == 3 and student_level <= 3:
                medium_priority.append(skill)

        print("\nHigh Priority Skills to Improve:")
        if high_priority:
            for skill in high_priority:
                print("-", skill)
        else:
            print("None")

        print("\nMedium Priority Skills:")
        if medium_priority:
            for skill in medium_priority:
                print("-", skill)
        else:
            print("None")

        # -----------------------------
        # Bar Chart Visualization
        # -----------------------------
        student_values = []
        company_values = []

        for skill in skills:
            student_values.append(student_skills[skill])
            company_values.append(selected_row[skill])

        x = np.arange(len(skills))

        plt.figure(figsize=(12, 6))
        plt.bar(x - 0.2, student_values, width=0.4, label="Student")
        plt.bar(x + 0.2, company_values, width=0.4, label="Company")

        plt.xticks(x, skills, rotation=45)
        plt.ylabel("Skill Level (1-5)")
        plt.title(f"Skill Comparison with {selected_company}")
        plt.legend()
        plt.tight_layout()
        plt.show()

        break


# -----------------------------
# College Mode
# -----------------------------
def college_mode():

    companies = load_companies()
    if companies is None:
        return

    skills = companies.columns[1:]

    while True:
        try:
            num_students = int(input("\nEnter number of students: "))
            if num_students > 0:
                break
            else:
                print("Enter a positive number.")
        except:
            print("Invalid input.")

    students_data = []

    print_skill_guide()

    for i in range(num_students):
        print(f"\nEntering data for Student {i+1}")
        name = input("Enter Name: ")
        roll = input("Enter Roll Number: ")

        student_skills = {}
        for skill in skills:
            student_skills[skill] = safe_skill_input(skill)

        students_data.append({
            "name": name,
            "roll": roll,
            "skills": student_skills
        })

    print("\nAvailable Companies:")
    for company in companies["Company"]:
        print("-", company)

    while True:
        selected_company = input("\nEnter company name for ranking or 'back': ")

        if selected_company.lower() == "back":
            return

        if selected_company not in companies["Company"].values:
            print("Invalid company. Try again.")
            continue

        selected_row = companies[companies["Company"] == selected_company].iloc[0]
        ranking = []

        for student in students_data:
            student_vector = np.array(list(student["skills"].values()))
            company_vector = np.array(selected_row[1:])

            score = np.dot(student_vector, company_vector)
            max_score = np.dot(np.ones(len(student_vector)) * 5, company_vector)

            alignment = (score / max_score) * 100 if max_score != 0 else 0

            ranking.append((student["name"], student["roll"], round(alignment, 2)))

        ranking.sort(key=lambda x: x[2], reverse=True)

        print(f"\nRanking for {selected_company}:")
        for rank, student in enumerate(ranking, start=1):
            print(f"{rank}. {student[0]} ({student[1]}) → {student[2]}%")

        break


# -----------------------------
# Main Menu
# -----------------------------
while True:
    print("\n===== MAIN MENU =====")
    print("1. Individual Student Mode")
    print("2. College Mode")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        individual_mode()
    elif choice == "2":
        college_mode()
    elif choice == "3":
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Try again.")