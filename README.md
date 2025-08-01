# NextEdge - Student Performance Dashboard

## Project Overview
NextEdge is a Python-based interactive dashboard application built with Streamlit to analyze student performance data. It helps educators and administrators monitor student progress, identify at-risk students, and provide actionable recommendations to improve academic outcomes.

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn
- Joblib

## Setup Instructions
1. Clone the repository.
2. Ensure you have Python 3.7 or higher installed.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

## Usage
- The dashboard allows you to:
  - View overall student statistics such as average attendance and predicted pass counts.
  - Search and select individual students to view detailed performance metrics.
  - See pass/fail predictions based on a trained machine learning model.
  - Get personalized recommendations to improve student performance.
  - Visualize performance breakdowns and prediction insights through interactive charts.
  - Predict future performance by inputting hypothetical values.
  - Upload updated student data CSV files and download the updated dataset.

## Data and Model
- The app uses a dataset (`student_performance_60.csv`) containing student assessment scores, attendance, participation, and previous grades.
- A machine learning model (Random Forest) is trained to predict student pass/fail outcomes based on these features.
- The model pipeline is saved as `model_pipeline.pkl` and loaded by the app for predictions.

## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, please contact the project maintainer.
