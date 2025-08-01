import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Student Dashboard", layout="wide")

# Function to generate smart tips
def generate_tip(student_data):
    tips = []
    if student_data["Attendance_Percentage"] < 60:
        tips.append("📌 Improve attendance.")
    if student_data["Internal_Assessment_1"] < 15:
        tips.append("📝 Focus on Internal 1 topics.")
    if student_data["Participation_Score"] < 5:
        tips.append("🙋‍♂️ Engage more in class.")
    return " | ".join(tips) if tips else "🎯 You're on track!"

# Load model and data
model = joblib.load("model_pipeline.pkl")
df = pd.read_csv("student_performance_60.csv")

# Light/Dark mode toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

mode_label = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
st.sidebar.button(mode_label, on_click=toggle_mode)

# Apply theme colors based on mode
if st.session_state.dark_mode:
    bg_color = "#0E1117"
    text_color = "#FFFFFF"
    chart_color_scale = "darkmint"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    chart_color_scale = "blues"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .sidebar .sidebar-content {{
        background-color: {bg_color};
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 Student Performance Dashboard")
st.markdown("Analyze student progress, identify risks, and provide recommendations.")

# Add overall stats
col1, col2, col3 = st.columns(3)
with col1:
    avg_attendance = round(df["Attendance_Percentage"].mean(), 2)
    st.metric("📅 Avg. Attendance (%)", avg_attendance)
with col2:
    pass_count = sum((model.predict(df[[
        "Internal_Assessment_1", "Internal_Assessment_2",
        "Attendance_Percentage", "Previous_Semester_Grade",
        "Participation_Score"
    ]]) >= 15))
    st.metric("✅ Students Predicted to Pass", pass_count)
with col3:
    st.metric("📈 Dataset Size", len(df))

st.markdown("---")

# Student selection
# Search bar
search_term = st.text_input("🔍 Search Student by Name:")
filtered_df = df[df["Name"].str.contains(search_term, case=False, na=False)] if search_term else df

# Student selection
selected_student = st.selectbox("🎓 Select a Student", filtered_df["Name"])

student_data = df[df["Name"] == selected_student].iloc[0]


student_data = df[df["Name"] == selected_student].iloc[0]
features = [[
    student_data["Internal_Assessment_1"],
    student_data["Internal_Assessment_2"],
    student_data["Attendance_Percentage"],
    student_data["Previous_Semester_Grade"],
    student_data["Participation_Score"]
]]

prediction = model.predict(features)[0]
result = "✅ Pass" if prediction >= 15 else "❌ Fail"

# Display result with colors
st.subheader(f"🎯 Prediction Result: {'🟢' if prediction >= 15 else '🔴'} {result}")
st.markdown(f"**💡 Recommendation:** {generate_tip(student_data)}")

# Expandable section for detailed data
with st.expander("📋 View Student Details"):
    st.dataframe(pd.DataFrame([student_data]))

# Charts (Bar)
st.markdown("### 📊 Performance Breakdown")
chart_df = pd.DataFrame({
    "Metrics": ["Internal 1", "Internal 2", "Attendance", "Previous Grade", "Participation"],
    "Values": [
        student_data["Internal_Assessment_1"],
        student_data["Internal_Assessment_2"],
        student_data["Attendance_Percentage"],
        student_data["Previous_Semester_Grade"],
        student_data["Participation_Score"]
    ]
})
fig = px.bar(chart_df, x="Metrics", y="Values", color="Values", text="Values", height=350, color_continuous_scale=chart_color_scale)
st.plotly_chart(fig, use_container_width=True)

# Additional prediction graphs
st.markdown("### 📈 Prediction Insights")
# ==========================
# 🔮 Predict Future Performance
# ==========================

st.markdown("## 🔮 Future Performance Prediction")

# Prepare input features for new predictions
with st.form("future_prediction_form"):
    st.markdown("### 🧪 Input Hypothetical/Estimated Values")

    col1, col2, col3 = st.columns(3)
    with col1:
        projected_attendance = st.slider("Projected Attendance (%)", 50, 100, int(student_data["Attendance_Percentage"]))
    with col2:
        projected_participation = st.slider("Projected Participation Score (0-10)", 0, 10, int(student_data["Participation_Score"]))
    with col3:
        projected_internal3 = st.slider("Expected Internal 3 Score", 0, 25, 15)

    submitted = st.form_submit_button("Predict Future Outcome")

    if submitted:
        # Assume internal 3 has a similar weight as internal 1 & 2
        internal_1 = student_data["Internal_Assessment_1"]
        internal_2 = student_data["Internal_Assessment_2"]
        previous_grade = student_data["Previous_Semester_Grade"]

        total_predicted_score = internal_1 + internal_2 + projected_internal3

        # Display Predictions
        st.markdown(f"### 🎯 **Total Predicted Internal Score:** `{total_predicted_score}/75`")
        st.markdown(f"### 📚 **Final Predicted Performance:** `{round(total_predicted_score / 75 * 100, 2)}%`")
        st.markdown(f"### 📅 **Predicted Attendance Compliance:** {'✅ Likely Satisfactory' if projected_attendance >= 75 else '⚠️ At Risk'}")

        if total_predicted_score >= 45:
            st.success("🚀 The student is likely to pass based on projected scores.")
        else:
            st.error("🔻 The student might need improvement to pass.")

        # Display radar/spider chart
        radar_df = pd.DataFrame({
            'Criteria': ['Internal 1', 'Internal 2', 'Internal 3 (Predicted)', 'Attendance', 'Participation'],
            'Score': [internal_1, internal_2, projected_internal3, projected_attendance / 100 * 25, projected_participation * 2.5]
        })

        fig_radar = px.line_polar(radar_df, r='Score', theta='Criteria', line_close=True,
                                  title="🧭 Projected Academic Balance Radar",
                                  color_discrete_sequence=["#EF553B" if not st.session_state.dark_mode else "#00CC96"])
        fig_radar.update_traces(fill='toself')
        st.plotly_chart(fig_radar, use_container_width=True)
# ==========================
# Prediction distribution histogram
predictions = model.predict(df[[
    "Internal_Assessment_1", "Internal_Assessment_2",
    "Attendance_Percentage", "Previous_Semester_Grade",
    "Participation_Score"
]])
pred_df = pd.DataFrame({"Prediction Score": predictions})
fig2 = px.histogram(pred_df, x="Prediction Score", nbins=20, title="Prediction Score Distribution", color_discrete_sequence=["#636EFA"] if not st.session_state.dark_mode else ["#00CC96"])
st.plotly_chart(fig2, use_container_width=True)

# Pass/Fail count pie chart
pass_fail_counts = pd.Series(predictions >= 15).value_counts().rename({True: "Pass", False: "Fail"})
fig3 = px.pie(names=pass_fail_counts.index, values=pass_fail_counts.values, title="Pass vs Fail Prediction", color=pass_fail_counts.index,
              color_discrete_map={"Pass": "#00CC96", "Fail": "#EF553B"})
st.plotly_chart(fig3, use_container_width=True)

# Upload new data
st.markdown("---")
uploaded_file = st.file_uploader("📤 Upload updated student data (.csv)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data updated successfully! Refresh the page to reload.")
    # Save the updated DataFrame to a new CSV file
    df.to_csv("updated_student_performance.csv", index=False)
    st.write("Updated data saved as 'updated_student_performance.csv'.")    
    # Add a download button for the updated CSV
    st.download_button(
        label="Download Updated Data",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="updated_student_performance.csv",
        mime="text/csv"
    )
# Add a footer
st.markdown("---")
st.markdown("© 2025 Student Performance Dashboard. All rights reserved.")