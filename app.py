import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="📚",
    layout="wide"
)

# Title and description
st.title("📚 Student Performance Predictor")
st.markdown("""
This app predicts a student's final grade based on:
- Study hours per week
- Attendance percentage
- Previous test score
- Assignments completed percentage
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Train Model", "Make Prediction", "Data Visualization"])

# Load or create data
@st.cache_data
def load_data():
    if os.path.exists('data/student_data.csv'):
        return pd.read_csv('data/student_data.csv')
    else:
        # Create sample data if file doesn't exist
        np.random.seed(42)
        n_students = 200
        
        data = {
            'study_hours': np.random.randint(1, 10, n_students),
            'attendance': np.random.randint(60, 100, n_students),
            'previous_score': np.random.randint(50, 95, n_students),
            'assignments_completed': np.random.randint(70, 100, n_students),
        }
        
        # Calculate final grade
        final_grades = []
        for i in range(n_students):
            grade = (
                data['study_hours'][i] * 3 +
                data['attendance'][i] * 0.4 +
                data['previous_score'][i] * 0.3 +
                data['assignments_completed'][i] * 0.2
            ) / 1.9
            
            grade += np.random.randint(-5, 5)
            grade = max(0, min(100, grade))
            final_grades.append(round(grade))
        
        data['final_grade'] = final_grades
        df = pd.DataFrame(data)
        
        # Create directories if they don't exist
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/student_data.csv', index=False)
        
        return df

# Load data
df = load_data()

# HOME PAGE
if page == "Home":
    
    st.header("Welcome to Student Performance Predictor!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Dataset Overview")
        st.write(f"Total students: {len(df)}")
        st.write(f"Features: {len(df.columns)-1}")
        st.write("Target: Final Grade")
    
    with col2:
        st.subheader("📈 Quick Stats")
        st.write(f"Average Final Grade: {df['final_grade'].mean():.2f}")
        st.write(f"Highest Grade: {df['final_grade'].max()}")
        st.write(f"Lowest Grade: {df['final_grade'].min()}")
    
    st.subheader("🔍 Sample Data")
    st.dataframe(df.head())
    
    st.subheader("📋 Feature Descriptions")
    
    st.write("""
    - Study Hours: Hours spent studying per week
    - Attendance: Percentage of classes attended
    - Previous Score: Previous test marks
    - Assignments Completed: Percentage completed
    - Final Grade: Predicted student grade
    """)

# TRAIN MODEL PAGE
elif page == "Train Model":
    
    st.header("🤖 Train Machine Learning Model")
    
    st.write("We are using Linear Regression Algorithm.")
    
    # Features and target
    X = df[['study_hours', 'attendance', 'previous_score', 'assignments_completed']]
    y = df['final_grade']
    
    # Split dataset
    test_size = st.slider("Select test data percentage", 10, 40, 20)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size/100,
        random_state=42
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"Training samples: {len(X_train)}")
    
    with col2:
        st.write(f"Testing samples: {len(X_test)}")
    
    # Train button
    if st.button("Train Model"):
        
        with st.spinner("Training model..."):
            
            # Create model
            model = LinearRegression()
            
            # Train model
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Save model
            os.makedirs('models', exist_ok=True)
            
            with open('models/model.pkl', 'wb') as f:
                pickle.dump(model, f)
            
            st.success("✅ Model trained successfully!")
            
            # Show metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("R² Score", f"{r2:.3f}")
            
            with col2:
                st.metric("Mean Squared Error", f"{mse:.2f}")
            
            with col3:
                st.metric("Accuracy", f"{r2*100:.1f}%")
            
            # Feature Importance
            st.subheader("📊 Feature Importance")
            
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': abs(model.coef_)
            }).sort_values('importance', ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            sns.barplot(
                data=feature_importance,
                x='importance',
                y='feature',
                ax=ax
            )
            
            ax.set_title("Feature Importance")
            
            st.pyplot(fig)

# PREDICTION PAGE
elif page == "Make Prediction":
    
    st.header("🎯 Predict Student Performance")
    
    # Check if model exists
    if not os.path.exists('models/model.pkl'):
        
        st.warning("⚠️ Please train the model first!")
    
    else:
        
        # Load model
        with open('models/model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        st.write("Enter student information:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            study_hours = st.slider("Study Hours", 1, 10, 5)
            attendance = st.slider("Attendance Percentage", 60, 100, 80)
        
        with col2:
            previous_score = st.slider("Previous Score", 50, 95, 70)
            assignments = st.slider("Assignments Completed %", 70, 100, 85)
        
        # Predict button
        if st.button("Predict Grade"):
            
            input_data = np.array([
                [
                    study_hours,
                    attendance,
                    previous_score,
                    assignments
                ]
            ])
            
            prediction = model.predict(input_data)[0]
            
            st.subheader("Prediction Result")
            
            st.metric(
                "Predicted Final Grade",
                f"{prediction:.1f}"
            )
            
            # Grade Result
            if prediction >= 90:
                st.success("🌟 Excellent! Grade A")
            
            elif prediction >= 80:
                st.success("😊 Very Good! Grade B")
            
            elif prediction >= 70:
                st.info("👍 Good! Grade C")
            
            elif prediction >= 60:
                st.warning("📚 Satisfactory. Grade D")
            
            else:
                st.error("⚠️ Needs Improvement. Grade F")

# VISUALIZATION PAGE
elif page == "Data Visualization":
    
    st.header("📊 Data Visualizations")
    
    # Histograms
    st.subheader("Feature Distributions")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    features = [
        'study_hours',
        'attendance',
        'previous_score',
        'final_grade'
    ]
    
    for idx, feature in enumerate(features):
        
        row = idx // 2
        col = idx % 2
        
        axes[row, col].hist(
            df[feature],
            bins=20,
            color='skyblue',
            edgecolor='black'
        )
        
        axes[row, col].set_title(feature)
    
    plt.tight_layout()
    
    st.pyplot(fig)
    
    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    correlation = df.corr()
    
    sns.heatmap(
        correlation,
        annot=True,
        cmap='coolwarm',
        ax=ax
    )
    
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Made with  by Urmila ❤️")