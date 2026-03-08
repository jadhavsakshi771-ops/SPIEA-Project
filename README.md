# SPIEA — Smart Placement Intelligence & Employability Analyzer

SPIEA is a Flask-based web application that helps students evaluate their **placement readiness** using academic metrics and resume-based skill analysis.
The system analyzes student data, extracts skills from uploaded resumes, and generates **placement predictions and analytics visualizations** through an interactive dashboard.

---

## 🚀 Features

* **User Authentication**

  * Student registration and login system
* **Resume Skill Analysis**

  * Extracts keywords from uploaded PDF resumes
* **Placement Prediction**

  * Calculates placement readiness score using:

    * CGPA
    * Skill score
    * Resume-detected skills
* **Interactive Dashboard**

  * Placement probability gauge
  * Placement score analytics chart
  * Skill strength radar chart
* **Student Records**

  * Stores analysis results in a SQLite database

---

## 🖥️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, Bootstrap, Chart.js
* **Database:** SQLite
* **Resume Parsing:** pdfminer.six

---

## 📂 Project Structure

```
SPIEA_project/
│
├── app.py
├── spiea.db
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│
├── static/
│   ├── style.css
│
└── uploads/
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/spiea-project.git
cd spiea-project
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the application

```
python app.py
```

### 4. Open in browser

```
http://127.0.0.1:5000
```

---

## 📊 How It Works

1. Users create an account and log in.
2. Students enter their **CGPA and skill score**.
3. Optional **resume upload** allows the system to detect additional skills.
4. The application calculates a **placement readiness score**.
5. Results are visualized through charts and analytics.

---

## 🎯 Use Case

SPIEA helps students understand their **employability readiness** and identify areas for improvement before placement drives.

---

## 📜 License

This project is developed for **educational and demonstration purposes**.

---

## 👩‍💻 Author

Developed by **Sakshi Jadhav**

✅ This version:  
- Resolves all Git merge conflicts  
- Includes **Render deployment instructions**  
- Clear, professional, and ready for GitHub  

---

If you want, I can also give you a **clean `requirements.txt` and `.gitignore`** ready to paste, so your Render deployment won’t fail.  

Do you want me to do that next?

## Deployment

- Ready for **Render.com free deployment**
- Environment variable: SECRET_KEY=spiea_secret_key
