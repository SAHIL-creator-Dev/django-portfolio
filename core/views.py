from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import re
import logging
from .models import Skill, Project, Experience, ContactMessage
import re
import logging

from django.conf import settings
from django.core.mail import send_mail
logger = logging.getLogger(__name__)


# ── Default data used when DB is empty (fresh install) ──────────────────────

DEFAULT_SKILLS = [
    # Languages
    {'name': 'Python',      'category': 'language',  'proficiency_label': 'core',        'proficiency': 95, 'icon': 'devicon-python-plain',      'order': 1},
    {'name': 'JavaScript',  'category': 'language',  'proficiency_label': 'comfortable',        'proficiency': 80, 'icon': 'devicon-javascript-plain',  'order': 2},
    {'name': 'HTML5',       'category': 'language',  'proficiency_label': 'comfortable',        'proficiency': 90, 'icon': 'devicon-html5-plain',       'order': 3},
    {'name': 'CSS3',        'category': 'language',  'proficiency_label': 'comfortable',        'proficiency': 85, 'icon': 'devicon-css3-plain',        'order': 4},
    # Frameworks
    {'name': 'Django',      'category': 'framework', 'proficiency_label': 'core',        'proficiency': 92, 'icon': 'devicon-django-plain',      'order': 5},
    # AI / ML
    {'name': 'NumPy',       'category': 'aiml',      'proficiency_label': 'comfortable', 'proficiency': 85, 'icon': 'devicon-python-plain',      'order': 6},
    {'name': 'Pandas',      'category': 'aiml',      'proficiency_label': 'comfortable',   'proficiency': 75, 'icon': 'devicon-pandas-original',   'order': 7},
    {'name': 'OpenCV',      'category': 'aiml',      'proficiency_label': 'exploring',   'proficiency': 70, 'icon': 'devicon-python-plain',      'order': 8},
    {'name': 'Machine Learning', 'category': 'aiml', 'proficiency_label': 'exploring',   'proficiency': 75, 'icon': 'devicon-python-plain',      'order': 9},
    {'name': 'AI Fundamentals',  'category': 'aiml', 'proficiency_label': 'exploring',   'proficiency': 80, 'icon': 'devicon-python-plain',      'order': 10},
    # Databases
    {'name': 'SQLite',      'category': 'database',  'proficiency_label': 'comfortable',        'proficiency': 88, 'icon': 'devicon-sqlite-plain',      'order': 11},
    {'name': 'MySQL',       'category': 'database',  'proficiency_label': 'comfortable', 'proficiency': 82, 'icon': 'devicon-mysql-plain',       'order': 12},
    # Tools
    {'name': 'Git',         'category': 'tool',      'proficiency_label': 'comfortable',        'proficiency': 88, 'icon': 'devicon-git-plain',         'order': 13},
    {'name': 'GitHub',      'category': 'tool',      'proficiency_label': 'comfortable',        'proficiency': 90, 'icon': 'devicon-github-original',    'order': 14},
]

DEFAULT_PROJECTS = [
    {
    'title': 'SK Martial Arts Academy',
    'description': 'Official website for a martial arts academy built with Django, providing a modern online presence with dynamic content management and responsive design.',
    'problem_solved': 'The academy lacked a professional website to showcase its programs, instructors, achievements, and contact information, making it difficult for prospective students to access information online.',
    'key_features': 'Responsive Website, Programs Showcase, Instructor Profiles, Gallery, Contact Form, Google Maps Integration, Django Admin CMS',
    'my_contribution': 'Designed and developed the complete website, implemented dynamic content management through Django Admin, optimized responsive layouts, configured production deployment, and managed static files and environment-based settings.',
    'tech_stack': 'Python, Django, HTML, CSS, JavaScript, SQLite',
    'github_url': 'https://github.com/yourusername/sk-martial-arts-academy',
    'live_url': 'https://your-live-url.com',
    'featured': True,
    'order': 2,
},
{
    'title': 'DomusCare',
    'description': 'A comprehensive Django-based relocation assistance platform that helps students, professionals, families, and individuals find rental accommodations and trusted local service providers when moving to a new city.',

    'problem_solved': 'People relocating to a new city often struggle to find reliable rental accommodations and trusted local services such as electricians, plumbers, cleaners, and technicians. DomusCare simplifies the relocation process by bringing housing and essential home services together on a single platform.',

    'key_features': 'User Authentication, Rental Property Listings, Verified Service Providers, Advanced Search & Filters, User Profiles, Contact Requests, Service Categories, Django Admin Dashboard',

    'my_contribution': 'Designed and developed the complete full-stack application using Django, created the database architecture, implemented authentication, rental and service management modules, advanced search functionality, and an intuitive responsive user interface.',

    'tech_stack': 'Python, Django, HTML, CSS, JavaScript, SQLite',

    'github_url': 'https://github.com/yourusername/DomusCare',

    'live_url': '',

    'featured': True,

    'order': 4,
},
{
    'title': 'Study Planner Agent',
    'description': 'AI-powered study planning assistant that helps students organize study schedules, manage tasks, and improve productivity through intelligent planning.',
    'problem_solved': 'Students often struggle to create structured study plans, prioritize subjects, and maintain consistency, resulting in inefficient learning and missed deadlines.',
    'key_features': 'AI Study Planner, Personalized Study Schedule, Task Management, Goal Tracking, Progress Monitoring, Smart Recommendations, Daily Planner',
    'my_contribution': 'Designed the application architecture, implemented intelligent study planning workflows, developed the backend logic, and created an intuitive user interface for effective study management.',
    'tech_stack': 'Python, Django, HTML, CSS, JavaScript, AI',
    'github_url': 'https://github.com/yourusername/study-planner-agent',
    'live_url': '',
    'featured': True,
    'order': 3,
},
    {
        'title': 'TransitOps',
        'description': 'Smart Transport Operations Platform designed to streamline scheduling, expense records, and logistics tracking.',
        'problem_solved': 'Inefficient vehicle scheduling, unmonitored driver trips, and manual expense logs led to excessive transport operational delays and overhead costs.',
        'key_features': 'Vehicle Management, Driver Management, Trip Management, Maintenance Tracking, Expense Tracking, Dashboard, Reports',
        'my_contribution': 'Designed the database relational models for vehicle trips and coded the automated monthly operational expense report generator.',
        'tech_stack': 'Python, Django, SQLite, Bootstrap',
        'github_url': 'https://github.com/sahilthapa/TransitOps',
        'live_url': '',
        'featured': True,
        'order': 6,
    },
    {
        'title': 'InfoNest',
        'description': 'Centralized Data Access Portal connecting academic portfolios, noticeboards, and tools.',
        'problem_solved': 'Students and faculty lacked a unified web interface to access portfolios, generate resumes, and view announcements, resulting in scattered communication.',
        'key_features': 'Student Portal, Faculty Portal, Authentication, Resume Generator, Student Profile, Notice Board, Gallery',
        'my_contribution': 'Built the resume builder parsing engines and developed the front-end profile dashboards.',
        'tech_stack': 'Python, Django, SQLite, HTML, CSS, JavaScript',
        'github_url': 'https://github.com/sahilthapa/InfoNest',
        'live_url': '',
        'featured': True,
        'order': 1,
    },
    {
        'title': 'Student Result Analysis System',
        'description': 'Analytical utility tool computing score averages, standard deviations, and class performance ranking models.',
        'problem_solved': 'Manually calculating class statistics, subject averages, and ranks for hundreds of students from raw CSV data sheets was highly tedious.',
        'key_features': 'Student Performance Analysis, Subject Statistics, Ranking System, Average Marks, NumPy Data Analysis',
        'my_contribution': 'Wrote the mathematical NumPy scripts to compute standard deviations, subject averages, and rank matrices.',
        'tech_stack': 'Python, NumPy',
        'github_url': 'https://github.com/sahilthapa/result-analysis',
        'live_url': '',
        'featured': False,
        'order': 5,
    },
]

DEFAULT_EXPERIENCE = [
    {
    'company': 'Freelance',
    'role': 'Python & Django Developer',
    'start_date': '2026',
    'end_date': 'Present',
    'description': 'Developed and deployed custom Django web applications for clients and personal projects, including the live SK Martial Arts Academy website. Experienced in backend development, responsive UI implementation, Django Admin customization, deployment, and database design.',
    'order': 1,
},
    {
        'company': 'Uttarakhand Technical University (UTU)',
        'role': 'B.Tech Computer Science Engineering (Lateral Entry)',
        'start_date': '2025',
        'end_date': 'Present',
        'description': 'Currently pursuing a B.Tech in Computer Science Engineering. Building production-ready Django applications, expanding expertise in Artificial Intelligence, Machine Learning, Computer Vision, and Data Analysis, while continuously strengthening backend development skills.',
        'order': 1,
    },
    {
        'company': 'Government Polytechnic Srinagar (UBTER)',
        'role': 'Diploma in Information Technology',
        'start_date': '2023',
        'end_date': '2025',
        'description': 'Built a strong foundation in Python programming, database management, web technologies, software engineering, networking, and object-oriented programming through academic projects and practical development.',
        'order': 2,
    },
    {
        'company': 'SBM Inter College, Rishikesh',
        'role': 'Higher Secondary Education (Class 12)',
        'start_date': '2023',
        'end_date': '2023',
        'description': 'Completed Higher Secondary Education with a focus on building the academic foundation that led to pursuing Information Technology and Computer Science.',
        'order': 3,
    },
]


def _seed_defaults():
    """Seed default data if DB tables are empty."""
    if not Skill.objects.exists():
        for s in DEFAULT_SKILLS:
            Skill.objects.create(**s)
    if not Project.objects.exists():
        for p in DEFAULT_PROJECTS:
            Project.objects.create(**p)
    if not Experience.objects.exists():
        for e in DEFAULT_EXPERIENCE:
            Experience.objects.create(**e)


def home(request):
    try:
        _seed_defaults()
        skills = Skill.objects.all()
        projects = Project.objects.all()
        experiences = Experience.objects.all()

        # Group skills by category
        skill_categories = {}
        for skill in skills:
            cat = skill.get_category_display()
            skill_categories.setdefault(cat, []).append(skill)

        context = {
            'skills': skills,
            'skill_categories': skill_categories,
            'projects': projects,
            'featured_projects': projects.filter(featured=True),
            'other_projects': projects.filter(featured=False),
            'experiences': experiences,
        }
    except Exception as e:
        logger.error(f"Error loading home page data: {e}")
        # If migrations haven't run yet, render with defaults only
        skill_categories = {}
        for s in DEFAULT_SKILLS:
            cat_label = dict(Skill.CATEGORY_CHOICES).get(s['category'], s['category'].title())
            skill_categories.setdefault(cat_label, []).append(type('Skill', (), s)())

        context = {
            'skills': DEFAULT_SKILLS,
            'skill_categories': skill_categories,
            'projects': [type('Project', (), {**p, 'get_tech_list': lambda self: [t.strip() for t in self.tech_stack.split(',')]})() for p in DEFAULT_PROJECTS],
            'featured_projects': [type('Project', (), {**p, 'get_tech_list': lambda self: [t.strip() for t in self.tech_stack.split(',')]})() for p in DEFAULT_PROJECTS if p['featured']],
            'other_projects': [type('Project', (), {**p, 'get_tech_list': lambda self: [t.strip() for t in self.tech_stack.split(',')]})() for p in DEFAULT_PROJECTS if not p['featured']],
            'experiences': [type('Experience', (), e)() for e in DEFAULT_EXPERIENCE],
        }

    return render(request, 'core/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        error_msg = None
        if not name or not email or not subject or not message:
            error_msg = 'All fields are required.'
        elif len(name) > 100 or len(subject) > 200:
            error_msg = 'Name or subject is too long.'
        elif len(message) > 5000:
            error_msg = 'Message is too long (maximum 5000 characters).'
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error_msg = 'Invalid email address format.'

        if not error_msg:
            try:
                send_mail(
                    subject=f"Portfolio Contact: {subject}",
                    message=f"""
            New message from your portfolio

            Name: {name}
            Email: {email}

            Message:
            {message}
            """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )

            except Exception as e:
                logger.exception("Failed to send contact email.")

                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "Sorry, something went wrong while sending your message.",
                        },
                        status=500,
                    )

                messages.error(
                    request,
                    "Sorry, something went wrong while sending your message.",
                )
                return redirect("home")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok', 'message': 'Message sent successfully!'})
            messages.success(request, 'Your message has been sent!')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
            messages.error(request, error_msg)

        return redirect('home')

    return redirect('home')
