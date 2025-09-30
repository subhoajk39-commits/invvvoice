![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![Made with Django](https://img.shields.io/badge/made%20with-Django-092E20.svg)

# 🧾 Invoice Management System

A modern, role-based, multi-tenant invoice management application built with Django and Django REST Framework. Tailored for international post-production teams, this system streamlines project tracking, work submissions, category-wise pricing, and professional invoice generation.

---

## ✨ Core Features

### 🔐 Role-Based Access Control

* **Super Admin**: Manages the entire system. Can create Admins and view all data.
* **Admin**: Manages their own team, client projects, categories, and pricing.
* **User**: Submits work entries assigned under Admin's projects.

### 🏗️ Project & Work Management

* Admins can create and manage multiple **Client Projects**.
* Users submit daily work under projects:

  * Folder Name
  * Quantity
  * Category (dropdown from Admin-defined list)
  * Date of Work
* Admins manage submitted work and assign pricing automatically by category.

### 💼 Category-Based Pricing

* Per-project category lists with flat rates.
* Admins can add, update, or remove categories.
* Pricing is calculated automatically based on quantity × category rate.

### 📄 Invoice Generation (Excel)

* Generate `.xlsx` invoices using filters:

  * Project
  * Date Range
  * Specific User
* Invoices can be downloaded and deleted from the Reports section.

### 📊 Dashboard & Reports

* Clean dashboard for Super Admins and Admins.
* Filtered views to see submitted work entries.
* Project-wise work breakdown, latest invoices, and entry tracking.
* Even you delete the projects then also the reports section you will found your downloaded data

### 🎨 UI/UX & Theming

* Fully responsive modern **Dark-Themed Dashboard UI**
* Pagination and scroll-to-top/bottom controls for better navigation
* Crisp styling with Bootstrap 5 and custom templates

### 🔐 Authentication

* Login system for all users
* Role-based data isolation
* Admins only see their own team's work

### 🧰 Developer-Friendly Codebase

* Django class-based views + decorators
* Clean app structure: `Invoice`, `Invoice_project`, `templates`, etc.
* API-ready with Django REST Framework & JWT support

---

## 🛠️ Technology Stack

| Component      | Technology                      |
| -------------- | ------------------------------- |
| **Backend**    | Python, Django                  |
| **API**        | Django REST Framework           |
| **Auth**       | JWT + Django Auth               |
| **Database**   | SQLite (Dev), PostgreSQL (Prod) |
| **Excel**      | OpenPyXL                        |
| **UI**         | Bootstrap 5 (Dark Theme)        |
| **Deployment** | *****************               |

---

## 🚀 Getting Started (Local Setup)

```bash
# 1. Clone the repo
https://github.com/aroyslipk/invoice-project.git
cd invoice-project

# 2. Setup virtual environment
python -m venv venv
venv\Scripts\activate  # (Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create Superuser (IMPORTANT)
python manage.py createsuperuser
# Then set their role to `super_admin` using `python manage.py shell`

# 6. Run the server
python manage.py runserver
```

---

## 📁 Project Structure (Simplified)

```
Invoice_project/
├── Invoice/            # Main app (models, views, templates)
├── templates/          # Global HTML templates
├── static/             # Custom CSS & JS
├── media/              # Uploaded invoice files
├── db.sqlite3
├── requirements.txt
└── manage.py
```

---

## 📜 License

This project is licensed under the MIT License.

> Copyright (c) 2025 AnikRoy
>
> Permission is hereby granted, free of charge, to any person obtaining a copy...

(See `LICENSE` file for full text)

---

## 👤 Author

**Anik Roy**
📧 [anik.byteinfo11@gmail.com](mailto:anik.byteinfo11@gmail.com)
🔗 GitHub: [@aroyslipk](https://github.com/aroyslipk)

---

✅ Built for international post-production professionals.
📌 Clean UI • Secure Architecture • Professional Output
