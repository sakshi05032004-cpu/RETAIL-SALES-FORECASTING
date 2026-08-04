# Big Mart Sales Prediction Using Machine Learning

## Overview

This project predicts the sales of products in Big Mart stores using Machine Learning.

The workflow includes:

- Data Cleaning
- Missing Value Treatment
- Exploratory Data Analysis (EDA)
- Feature Encoding
- Model Training using XGBoost Regressor
- Model Evaluation
- Model Saving using Pickle

---

## Dataset

Big Mart Sales Dataset

Features include:

- Item Identifier
- Item Weight
- Item Fat Content
- Item Visibility
- Item Type
- Item MRP
- Outlet Identifier
- Outlet Size
- Outlet Type
- Outlet Establishment Year
- Outlet Location Type

Target:

- Item Outlet Sales

---

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- XGBoost
- Pickle

---

## Machine Learning Algorithm

- XGBoost Regressor

---

## Project Workflow

1. Load dataset
2. Handle missing values
3. Perform EDA
4. Encode categorical variables
5. Split training and testing data
6. Train XGBoost model
7. Evaluate using R² Score
8. Save trained model

---

## Project Structure


BigMart-Sales-Prediction/
│── data/
│── notebooks/
│── models/
│── train.py
│── predict.py
│── requirements.txt
│── README.md


---

## Installation

bash
git clone https://github.com/yourusername/BigMart-Sales-Prediction.git

cd BigMart-Sales-Prediction

pip install -r requirements.txt


---

## Run Training

bash
python train.py


---

## Predict

bash
python predict.py


---

## Model Performance

Evaluation Metric:

- R² Score

---

## Future Improvements

- Hyperparameter tuning
- Streamlit Web App
- Docker Deployment
- Feature Engineering
- Model Comparison
