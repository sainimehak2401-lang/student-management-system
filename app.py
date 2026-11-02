
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="AI Student Management System",
    page_icon="🎓",
    layout="wide"
)

DATA_FILE = Path("data/students.csv")

st.markdown("""
<style>
.stApp { background-color: #f4f7fb; }
.block-container { padding-top: 2rem; }
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #dce3ed;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_students():
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()


st.title("🎓 Student Management System")
st.caption("Student records • Marks • Results • Academic analytics")

if not DATA_FILE.exists():
    st.error("Student data not found. Please run python seed_data.py first.")
    st.stop()

df = load_students()

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Student Records", "Marks & Results", "AI Study Assistant"]
)

st.sidebar.success(f"{len(df)} demo student records loaded")

if page == "Dashboard":
    st.subheader("Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students", len(df))
    c2.metric("Average Percentage", f"{df['percentage'].mean():.1f}%")
    c3.metric("Pass Students", int((df["result"] == "PASS").sum()))
    c4.metric("Fail Students", int((df["result"] == "FAIL").sum()))

    st.subheader("Student Performance")
    st.bar_chart(df.groupby("course")["percentage"].mean())

    st.subheader("Recent Student Records")
    st.dataframe(
        df[["student_id", "name", "course", "semester", "percentage", "result"]].head(10),
        use_container_width=True,
        hide_index=True
    )

elif page == "Student Records":
    st.subheader("Student Directory")

    search = st.text_input("Search by student name or ID")
    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["name"].str.contains(search, case=False, na=False)
            | filtered["student_id"].str.contains(search, case=False, na=False)
        ]

    st.write(f"Found {len(filtered)} students")

    for _, student in filtered.iterrows():
        with st.expander(f"{student['student_id']} — {student['name']}"):
            left, right = st.columns([1, 3])

            with left:
                initials = "".join(
                    part[0] for part in str(student["name"]).split()[:2]
                ).upper()
                st.markdown(
                    f"<div style='width:90px;height:90px;border-radius:50%;"
                    f"background:#dbeafe;color:#1d4ed8;display:flex;"
                    f"align-items:center;justify-content:center;"
                    f"font-size:28px;font-weight:bold'>{initials}</div>",
                    unsafe_allow_html=True
                )

            with right:
                st.write(f"**Email:** {student['email']}")
                st.write(f"**Course:** {student['course']}")
                st.write(f"**Semester:** {student['semester']}")
                st.write(f"**Attendance:** {student['attendance']}%")
                st.write(f"**Percentage:** {student['percentage']}%")
                st.write(f"**Result:** {student['result']}")

elif page == "Marks & Results":
    st.subheader("Subject-wise Marks and Results")

    student_id = st.selectbox("Select Student ID", df["student_id"].tolist())
    student = df[df["student_id"] == student_id].iloc[0]

    st.write(f"### {student['name']} ({student['student_id']})")

    subject_columns = [
        col for col in df.columns if col.endswith("_marks")
    ]

    marks_data = []
    for col in subject_columns:
        subject_name = col.removesuffix("_marks")
        marks_data.append({
            "Subject": subject_name,
            "Marks Obtained": int(student[col]),
            "Maximum Marks": 100,
            "Status": "PASS" if student[col] >= 40 else "FAIL"
        })

    st.dataframe(
        pd.DataFrame(marks_data),
        use_container_width=True,
        hide_index=True
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Marks", f"{student['total_marks']} / {student['maximum_marks']}")
    c2.metric("Percentage", f"{student['percentage']:.2f}%")
    c3.metric("Overall Result", student["result"])

    st.progress(min(float(student["percentage"]) / 100, 1.0))

    st.download_button(
        "Download Student Result CSV",
        data=pd.DataFrame([student]).to_csv(index=False),
        file_name=f"{student_id}_result.csv",
        mime="text/csv"
    )

elif page == "AI Study Assistant":
    st.subheader("🤖 Academic Study Assistant")

    student_id = st.selectbox("Choose Student", df["student_id"].tolist())
    student = df[df["student_id"] == student_id].iloc[0]

    st.write(f"Study recommendations for **{student['name']}**")

    weak_subjects = [
        col.removesuffix("_marks")
        for col in df.columns
        if col.endswith("_marks") and student[col] < 60
    ]

    if weak_subjects:
        st.warning("Subjects to focus on: " + ", ".join(weak_subjects))
        for subject in weak_subjects:
            st.write(f"- {subject}: revise concepts and practice questions.")
    else:
        st.success("Marks are at least 60 in all listed subjects.")

    st.info(
        "These are rule-based study suggestions, not a trained AI prediction. "
        "Advanced AI will be added in a later step."
    )

st.divider()
st.caption("Development demo • Sample data only")
