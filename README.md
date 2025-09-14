📘 InterviewHub

InterviewHub is a Python desktop application where users can register, log in, and share their interview experiences.
The app uses Tkinter for GUI and MySQL for database storage.


🚀 Features


🔐 User Authentication

Register new users (unique username, secure password)

Login with credentials


📝 Interview Experiences

Add interview experiences (company, role, difficulty, summary)

View all experiences

Search experiences by company or keyword


🎨 User-Friendly GUI

Built using Tkinter

Separate screens for Login/Register and Dashboard


🛠️ Tech Stack

Python 3.x

Tkinter – GUI

MySQL – Database

mysql-connector-python – Database connection



📂 Database Schema
CREATE DATABASE experience_app;

USE experience_app;


CREATE TABLE users (

    id INT AUTO_INCREMENT PRIMARY KEY,    
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE experiences (

    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    experience TEXT NOT NULL,
    difficulty VARCHAR(50),
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    
);


📦 Installation

Clone the repository

git clone https://github.com/your-username/interviewhub.git
    
cd interviewhub


Install dependencies

pip install mysql-connector-python==9.4.0 


Configure database connection

Edit config.py with your MySQL username, password, and host

db_config = {

    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "experience_app"
}


Run the app

python app.py
