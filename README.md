# 🍽️ FoodSphere – Food Court Management System

FoodSphere is a **Django-based Food Court Management System** designed for campuses and institutions.  
It provides a centralized platform where **admins manage vendors**, **vendors manage food items**, and **students place orders seamlessly**.

---

## 🚀 Features

### 👨‍💼 Admin
- Admin dashboard
- Approve / reject vendor shop requests
- Manage vendors, food items, and orders
- Full system control

### 🧑‍🍳 Vendor
- Apply for shop registration
- Add, update, and manage food items
- Set availability and preparation time
- View incoming orders

### 🎓 Student
- Browse food menus
- Place food orders
- View order status
- Simple and user-friendly interface

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (development)
- **Authentication:** Django Authentication System
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
FoodSphere/
├── accounts/              # User authentication & roles
├── vendors/               # Vendor & shop management
├── menu/                  # Food items & categories
├── orders/                # Order handling
├── foodcourt_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How to Run the Project Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Aman-0402/FoodSphere.git
cd FoodSphere
```

### 2️⃣ Create & activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations
```bash
python manage.py migrate
```

### 5️⃣ Create superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the server
```bash
python manage.py runserver
```

Visit 👉 http://127.0.0.1:8000/

---

## 📌 Project Status

✅ Completed  
🚀 Open for enhancements (online payments, notifications, deployment)

---

## 🙌 Author

**Aman Raj**  
Web Developer | Python & Django | Full Stack Enthusiast

GitHub: https://github.com/Aman-0402

---

## ⭐ Support

If you like this project, don't forget to give it a ⭐ on GitHub!