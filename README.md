# Professional Student Management System

A modern, creative, and efficient Student Management System built with **FastAPI** and a clean, professional **Tailwind CSS** frontend. This application provides robust features for managing student records with real-time updates and Python-driven analytics.

## 🚀 Key Features

### 📊 Core Management
- **Add, Update, & Delete**: Full CRUD operations for student records.
- **Dynamic Course Selection**: Dropdown with various academic courses (BCA, BBA, B.Tech, etc.).
- **Real-time Statistics**: Instant dashboard updates for total students, average CGPA, and course distribution.

### 🧠 Python-Powered Intelligence
- **Automated Grade Classification**: Python logic automatically assigns grades (A+, A, B, C, D, F) based on CGPA.
- **Top Performers Analytics**: Real-time identification of high-achieving students (CGPA > 8.5).
- **Search-Based Filtering**: Search across names, emails, and courses with immediate UI feedback.

### 📥 Data Operations
- **Smart CSV Export**: Export all records or only your current search results to a CSV file.
- **Bulk Import**: Quickly upload multiple student records via CSV for efficient management.
- **JSON Storage**: Lightweight and reliable data persistence in `students.json`.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Tailwind CSS, Inter Font, Vanilla JavaScript
- **Data Format**: JSON (Records), CSV (Export/Import)
- **Web Server**: Uvicorn

## 📋 Installation & Setup

1. **Clone the project** to your local machine.
2. **Navigate to the directory**:
   ```bash
   cd Student
   ```
3. **Install dependencies**:
   ```bash
   py -m pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   py main.py
   ```
5. **Access the system**:
   Open your browser and go to `http://127.0.0.1:8001`

## 📁 Project Structure
- `main.py`: The core FastAPI application containing API endpoints and Python logic.
- `templates/index.html`: The professional, responsive UI built with Tailwind CSS.
- `students.json`: The database file where student records are stored.
- `requirements.txt`: Project dependencies.

---
*Developed with a focus on professional aesthetics and functional efficiency.*
