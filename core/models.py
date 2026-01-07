from django.db import models


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(Timestamped):
    full_name = models.CharField(max_length=120)
    title = models.CharField(max_length=160)
    summary = models.TextField(blank=True)
    headshot = models.ImageField(upload_to="profile/", blank=True, null=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    resume_file = models.FileField(upload_to="docs/", blank=True, null=True)

    def __str__(self):
        return self.full_name


class SocialLink(Timestamped):
    label = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=80, blank=True)  # e.g. "bi bi-github"
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ["order", "label"]


class SkillCategory(Timestamped):
    name = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "name"]


class Skill(Timestamped):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=80)
    level = models.PositiveSmallIntegerField(default=0)  # 0–100
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        ordering = ["category__order", "order", "name"]


class Project(Timestamped):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=240, blank=True)  # comma-separated tags
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "-featured", "-created_at"]


class Experience(Timestamped):
    company = models.CharField(max_length=160)
    role = models.CharField(max_length=160)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.role} @ {self.company}"

    class Meta:
        ordering = ["order", "-start_date"]


class Education(Timestamped):
    school = models.CharField(max_length=160)
    program = models.CharField(max_length=160)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.program} - {self.school}"

    class Meta:
        ordering = ["order", "-start_date"]


class Certification(Timestamped):
    name = models.CharField(max_length=160)
    issuer = models.CharField(max_length=160, blank=True)
    issue_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order", "-issue_date", "name"]


class Service(Timestamped):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=80, blank=True)  # e.g., "bi bi-code-slash"
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "title"]


class ContactMessage(Timestamped):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"
