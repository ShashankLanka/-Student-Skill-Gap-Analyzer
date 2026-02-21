import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Placement Skill Alignment System", layout="wide")

st.title("🎓 Placement Skill Alignment Dashboard")
st.markdown("Analyze student skills against company requirements.")

# -----------------------------
# Sidebar Configuration
# -----------------------------
st.sidebar.header("Configuration")

branch = st.sidebar.selectbox("Select Branch", ["CSE", "EEE", "ECE", "MECH"])

if branch == "CSE":
    companies = pd.read_csv("CSE_companies.csv")
elif branch == "EEE":
    companies = pd.read_csv("EEE_companies.csv")
elif branch == "ECE":
    companies = pd.read_csv("ECE_companies.csv")
elif branch == "MECH":
    companies = pd.read_csv("MECH_companies.csv")

skills = companies.columns[1:]
mode = st.sidebar.radio("Select Mode", ["Individual Mode", "College Mode"])

# =====================================================
# INDIVIDUAL MODE
# =====================================================
if mode == "Individual Mode":

    st.header("👤 Individual Skill Analysis")

    student_skills = {}
    cols = st.columns(3)

    for i, skill in enumerate(skills):
        student_skills[skill] = cols[i % 3].slider(skill, 1, 5, 3)

    if st.button("Analyze Alignment"):

        student_vector = np.array(list(student_skills.values()))
        results = {}

        for index, row in companies.iterrows():
            company_name = row["Company"]
            company_vector = np.array(row[1:])

            score = np.dot(student_vector, company_vector)
            max_score = np.dot(np.ones(len(student_vector)) * 5, company_vector)

            alignment = (score / max_score) * 100 if max_score != 0 else 0
            results[company_name] = round(alignment, 2)

        sorted_results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

        st.subheader("📊 Alignment Results")
        result_df = pd.DataFrame(list(sorted_results.items()), columns=["Company", "Alignment %"])
        st.dataframe(result_df, use_container_width=True)

        # Download Alignment
        csv_alignment = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Alignment Report",
            data=csv_alignment,
            file_name="alignment_report.csv",
            mime="text/csv"
        )

        selected_company = st.selectbox("Select Company for Detailed Analysis", companies["Company"])
        selected_row = companies[companies["Company"] == selected_company].iloc[0]

        st.subheader(f"📌 Detailed Skill Analysis for {selected_company}")

        high_priority = []
        medium_priority = []

        for skill in skills:
            company_requirement = selected_row[skill]
            student_level = student_skills[skill]
            gap = company_requirement - student_level

            if gap > 0:
                status = f"Need +{gap}"
            elif gap == 0:
                status = "Perfect"
            else:
                status = "Exceeds"

            st.write(f"{skill} → Required: {company_requirement}, "
                     f"Your Level: {student_level}, Status: {status}")

            if company_requirement >= 4 and student_level <= 3:
                high_priority.append(skill)
            elif company_requirement == 3 and student_level <= 3:
                medium_priority.append(skill)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔥 High Priority Skills")
            st.write(high_priority if high_priority else "None")

        with col2:
            st.subheader("⚡ Medium Priority Skills")
            st.write(medium_priority if medium_priority else "None")

        # Bar Chart
        student_values = list(student_skills.values())
        company_values = list(selected_row[1:])

        fig, ax = plt.subplots(figsize=(10, 5))
        x = np.arange(len(skills))

        ax.bar(x - 0.2, student_values, width=0.4, label="Student")
        ax.bar(x + 0.2, company_values, width=0.4, label="Company")

        ax.set_xticks(x)
        ax.set_xticklabels(skills, rotation=45)
        ax.set_ylabel("Skill Level")
        ax.set_title(f"Skill Comparison with {selected_company}")
        ax.legend()

        st.pyplot(fig)

        # -----------------------------
        # Improvement Simulation
        # -----------------------------
        st.subheader("📈 Skill Improvement Impact Analysis")

        current_alignment = sorted_results[selected_company]
        impact_results = {}

        for skill in skills:
            if student_skills[skill] < 5:
                temp_skills = student_skills.copy()
                temp_skills[skill] += 1

                temp_vector = np.array(list(temp_skills.values()))
                company_vector = np.array(selected_row[1:])

                new_score = np.dot(temp_vector, company_vector)
                max_score = np.dot(np.ones(len(temp_vector)) * 5, company_vector)

                new_alignment = (new_score / max_score) * 100 if max_score != 0 else 0

                impact = round(new_alignment - current_alignment, 2)
                impact_results[skill] = impact

        impact_sorted = sorted(impact_results.items(), key=lambda x: x[1], reverse=True)
        impact_df = pd.DataFrame(impact_sorted, columns=["Skill", "Alignment Increase (%)"])

        st.dataframe(impact_df, use_container_width=True)

        # Download Impact
        csv_impact = impact_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Impact Analysis Report",
            data=csv_impact,
            file_name="impact_analysis_report.csv",
            mime="text/csv"
        )


# =====================================================
# COLLEGE MODE
# =====================================================
elif mode == "College Mode":

    st.header("🏫 College Ranking Mode")

    num_students = st.number_input("Number of Students", min_value=1, step=1)
    students_data = []

    for i in range(num_students):
        st.markdown(f"### Student {i+1}")
        name = st.text_input(f"Name {i}", key=f"name{i}")
        roll = st.text_input(f"Roll No {i}", key=f"roll{i}")

        student_skills = {}
        cols = st.columns(3)

        for j, skill in enumerate(skills):
            student_skills[skill] = cols[j % 3].slider(
                f"{skill} - Student {i+1}", 1, 5, 3, key=f"{skill}{i}"
            )

        students_data.append({
            "name": name,
            "roll": roll,
            "skills": student_skills
        })

    selected_company = st.selectbox("Select Company for Ranking", companies["Company"])

    if st.button("Generate Ranking"):

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
        ranking_df = pd.DataFrame(ranking, columns=["Name", "Roll No", "Alignment %"])

        st.subheader(f"📊 Ranking for {selected_company}")
        st.dataframe(ranking_df, use_container_width=True)

        # Download Ranking
        csv_ranking = ranking_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Ranking Report",
            data=csv_ranking,
            file_name="college_ranking_report.csv",
            mime="text/csv"
        )