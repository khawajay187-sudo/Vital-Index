#  Vital Index (Obesity Level Predictor)

Vital Index is a machine learning–powered web application that predicts a person's obesity level based on their lifestyle habits, eating patterns, physical activity, and daily routine. Built with Streamlit and powered by a Random Forest model trained on a large lifestyle dataset, the app also provides personalized health guidance to help users understand and improve their well-being.

🔗 **Live App:** [vital-index-healthchecker.streamlit.app](https://vital-index-healthchecker.streamlit.app/)

---

##  Overview

Obesity is influenced by far more than just height and weight daily habits like diet, physical activity, transportation, water intake, and screen time all play a role. Vital Index takes these lifestyle factors as input and uses a trained machine learning model to predict the user's obesity category, then offers actionable insights based on the result.

---

##  Features

- **Obesity Level Prediction**
  Predicts obesity category based on 16 lifestyle and physical attributes using a trained Random Forest model.

- **Health Tips**
  Provides curated tips and suggestions tailored to the user's predicted result.

- **Health Information**
  Detailed explanations of each obesity level/category, helping users understand what their result actually means.

- **Weight Loss Tips**
  Practical, easy-to-follow guidance for users looking to improve their lifestyle and reduce health risks.

---

##  How It Works

The app collects the following inputs from the user:

| Feature | Description |
|---|---|
| `Age` | Age of the user |
| `Height` | Height in meters |
| `Weight` | Weight in kilograms |
| `Gender` | Male / Female |
| `FAVC` | Frequent consumption of high-caloric food |
| `FCVC` | Frequency of vegetable consumption |
| `NCP` | Number of main meals per day |
| `SMOKE` | Smoking habit |
| `CH2O` | Daily water consumption |
| `SCC` | Calorie consumption monitoring |
| `family_history_with_overweight` | Family history of being overweight |
| `FAF` | Physical activity frequency |
| `TUE` | Time using technology devices |
| `CALC` | Alcohol consumption frequency |
| `CAEC` | Eating between meals |
| `MTRANS` | Primary mode of transportation |

These inputs are passed to a **Random Forest** model trained on a large, real-world lifestyle dataset, which then predicts the user's obesity category with high accuracy.

**Example input:**
```python
{
    'Age': 25, 'Height': 1.70, 'Weight': 70,
    'Gender': 'Male', 'FAVC': 'no', 'FCVC': 2.0, 'NCP': 3.0,
    'SMOKE': 'no', 'CH2O': 2.0, 'SCC': 'no',
    'family_history_with_overweight': 'no', 'FAF': 1.0, 'TUE': 1.0,
    'CALC': 'no', 'CAEC': 'Sometimes', 'MTRANS': 'Public_Transportation'
}
```

---

##  Tech Stack

| Category | Technology |
|---|---|
| **Frontend / App Framework** | [Streamlit](https://streamlit.io/) |
| **Data Handling** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (Random Forest) |
| **Model Serialization** | Joblib |
| **Visualization** | Plotly |
| **Language** | Python |

---

##  Project Structure

```
vital-index/
│
├── app/
│   ├── app.py              # Main Streamlit application
│   └── ...                 # Supporting modules / assets
│
├── requirements.txt        # Python dependencies
└── README.md                # Project documentation
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/khawajay187-sudo/vital-index.git
cd vital-index
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app/app.py
```

The app will be available at `http://localhost:8501`.

---

##  Live Demo

Try the app live here 👉 **[Vital Index](https://vital-index-healthchecker.streamlit.app/)**

---

##  Model Details

- **Algorithm:** Random Forest
- **Training Data:** Large-scale lifestyle and demographic dataset
- **Input Features:** 16 lifestyle, dietary, and physical parameters
- **Output:** Predicted obesity level/category

---

##  Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues) or submit a pull request.

---

##  Author

Developed by **Yasir Ali** with ❤️ using Python and Streamlit.

