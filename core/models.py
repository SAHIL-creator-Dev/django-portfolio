from django.db import models


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('language', 'Languages'),
        ('framework', 'Frameworks'),
        ('aiml', 'AI / ML'),
        ('database', 'Databases'),
        ('tool', 'Tools'),
    ]
    PROFICIENCY_LABELS = [
        ('core', 'Advanced'),
        ('comfortable', 'Intermediate'),
        ('exploring', 'Beginner'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tool')
    proficiency_label = models.CharField(max_length=20, choices=PROFICIENCY_LABELS, default='comfortable')
    proficiency = models.IntegerField(default=80, help_text="0-100 percentage")
    icon = models.CharField(max_length=100, blank=True, help_text="Devicon class e.g. devicon-python-plain")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    problem_solved = models.TextField(blank=True, help_text="Problem solved by this project")
    key_features = models.TextField(blank=True, help_text="Comma-separated list of key features")
    my_contribution = models.TextField(blank=True, help_text="Your contribution to this project")
    tech_stack = models.CharField(max_length=300, help_text="Comma-separated list")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',')]

    def get_features_list(self):
        if not self.key_features:
            return []
        return [f.strip() for f in self.key_features.split(',')]


class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20, default='Present')
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.role} at {self.company}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
