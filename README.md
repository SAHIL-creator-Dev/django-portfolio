# 🚀 Sahil Thapa — AI Software Developer Portfolio

A modern, Django-powered personal portfolio website featuring a clean dark aesthetic, terminal-style components, smooth scroll animations, and dynamic content management.

## 📖 Project Overview

This is my personal portfolio built to showcase my technical skills, projects, and educational journey. It demonstrates my ability to build clean, maintainable, and production-ready web applications using Django, while integrating a sleek frontend design.

## ✨ Features

- **Dynamic Content Management:** Easily update skills, projects, and experience via the Django Admin panel.
- **Modern UI/UX:** Clean dark theme with terminal/code aesthetic and AOS scroll animations.
- **Responsive Design:** Fully mobile-friendly layout.
- **Contact Form:** Integrated contact form with server-side validation and AJAX support.
- **SEO & Performance Optimized:** Configured with canonical URLs, meta tags, lazy loading, and WhiteNoise for static files.
- **Secure:** Enforces strong security headers, CSRF protection, and environment variable configuration.

## 🛠 Tech Stack

- **Backend:** Django 4.x, Python 3.10+
- **Database:** SQLite (Development) / Configurable for PostgreSQL
- **Frontend:** HTML5, Vanilla CSS3, JavaScript (AJAX)
- **Animations:** AOS (Animate On Scroll) 2.3.4
- **Icons:** Devicons 2.x
- **Fonts:** Inter, JetBrains Mono, Space Grotesk
- **Deployment Ready:** Configured with WhiteNoise and python-dotenv.

---

## ⚙️ Installation & Running Locally

Follow these steps to set up the project on your local machine.

### 1. Clone the repository
```bash
git clone https://github.com/SAHIL-creator-Dev/django-portfolio.git
cd portfolio
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables
Copy the example environment file and customize it:
```bash
cp .env.example .env
```
Inside `.env`, make sure to set:
- `DJANGO_SECRET_KEY`: A secure random string.
- `DJANGO_DEBUG`: `True` for local development.
- `DJANGO_ALLOWED_HOSTS`: `127.0.0.1,localhost`

### 5. Run Migrations & Seed Data
```bash
python manage.py migrate
```
*(Note: The database will automatically seed with default skills and projects when you first visit the homepage, provided migrations have been run.)*

### 6. Create a Superuser (For Admin Access)
```bash
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000** in your browser!

---

## 🚀 Deployment

This project is configured to be easily deployable to platforms like Render, Railway, or a VPS.

### Deployment Checklist:
1. Set up your host's environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS=yourdomain.com`).
2. Collect static files (handled automatically by most PaaS, or run `python manage.py collectstatic`).
3. Run migrations on the production database.
4. Use a production WSGI server like `gunicorn portfolio.wsgi`.

---

## 📸 Screenshots

*(Add screenshots of your portfolio here once deployed)*
- Hero Section
- Projects Grid
- Contact Form

## 🌐 Links

- **Live Demo:** *(Add link here)*
- **Resume:** Included in `core/static/core/resume/`
- **LinkedIn:** [Sahil Thapa](https://www.linkedin.com/in/sahil-thapa-107111369/)
- **GitHub:** [SAHIL-creator-Dev](https://github.com/SAHIL-creator-Dev)

## 📄 License
This project is open-source and available under the MIT License. Feel free to use it as inspiration!
