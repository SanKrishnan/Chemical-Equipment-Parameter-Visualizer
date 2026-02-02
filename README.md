# 📘 Chemical Equipment Parameter Visualizer

A complete end-to-end system for **uploading, analyzing, visualizing, and generating reports** for chemical equipment parameters.

This project integrates the following components:

- **React Frontend Dashboard**
- **Django REST Framework Backend (JWT Authentication)**
- **Python Desktop Application (Tkinter / PyQt5)**
- **CSV Upload + Summary Stats + Graphs + PDF Reports**

---
## Demo Video
https://drive.google.com/file/d/1URDCB_3-lS4yn-wmLr0kw-ExfEowcZvW/view?usp=drive_link

---
## 📂 Project Architecture
```bash
Chemical-Equipment-Parameter-Visualizer/
│
├── backend/               # Django REST API
│   ├── api/               # Upload, summary, authentication endpoints
│   ├── settings.py        # JWT, CORS, media storage
│   ├── db.sqlite3
│   └── ...
│
├── frontend/              # React Dashboard
│   ├── src/
│   │   ├── App.js
│   │   ├── components/    # Dashboard, Login, CSV Upload, History
│   │   └── ...
│   └── package.json
│
├── desktop_app/           # Python Desktop Application
│   ├── app.py             # GUI + PDF generation
│   ├── templates/
│   └── ...
│
├── requirements.txt
└── README.md

```
---

## 🚀 Features

### 🔹 React Frontend
- JWT login
- CSV file upload
- Summary statistics visualization
- Pie charts (type distribution)
- Real-time JSON summary viewer
- Upload history page
- Responsive UI

### 🔹 Django Backend (REST API)
- JWT-based authentication (SimpleJWT)
- CSV parsing & validation with Pandas
- Summary metrics:
  - Total entries
  - Average pressure, temperature, flowrate
  - Equipment type distribution
- Stores upload history
- Generates PDF reports on request
- CORS enabled

### 🔹 Python Desktop Application
- Login screen with masked password
- CSV upload from desktop
- Summary display
- Side-by-side charts (Pie + Bar)
- Custom “Save As...” PDF generation
- Error handling and user-friendly prompts

---

## 🛠 Tech Stack

### Frontend
- React.js
- Axios
- Chart.js
- HTML5 + CSS3

### Backend
- Python 3
- Django
- Django REST Framework
- SimpleJWT
- Pandas

### Desktop App
- Python 3
- Tkinter / PyQt5
- Matplotlib
- Requests
- ReportLab

---

## 📦 Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/Chemical-Equipment-Parameter-Visualizer.git
cd Chemical-Equipment-Parameter-Visualizer
```

## 🖥 Backend Setup (Django)
``` bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at: http://127.0.0.1:8000/

## 🌐 Frontend Setup (React)
cd frontend
npm install
npm start


Frontend runs at: http://localhost:3000/

## 🖥 Desktop App Setup
cd desktop_app
pip install -r requirements.txt
python app.py

## 🔗 API Endpoints
| Method | Endpoint            | Description          |
| ------ | ------------------- | -------------------- |
| POST   | `/api/token/`       | Login (JWT token)    |
| POST   | `/api/upload/`      | Upload CSV file      |
| GET    | `/api/history/`     | Fetch upload history |
| GET    | `/api/report/<id>/` | Download PDF report  |

## 📊 Summary Response Format
```bash
{
  "total_count": 15,
  "columns": [
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature"
  ],
  "avg_flowrate": 119.8,
  "avg_pressure": 6.1,
  "avg_temperature": 117.4,
  "type_distribution": {
    "Pump": 4,
    "Valve": 3,
    "Compressor": 2,
    "Reactor": 2,
    "HeatExchanger": 2,
    "Condenser": 2
  }
}
```
## 📝 PDF Report (Desktop App)

The desktop application generates a PDF report containing:

- Summary statistics

- Pie chart / Bar chart

- Timestamp

- Uploaded CSV entries

- User details (optional)

To customize save location:

``` bash
pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf")
```

## 👩‍💻 Contributors

Sanjana Krishnan

📄 License

Licensed under the MIT License.
