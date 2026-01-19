from django.db import models
from ordered_model.models import OrderedModel


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

    @property
    def display_image(self):
        if self.headshot and hasattr(self.headshot, 'name'):
            # Check if the raw value is a full URL
            if str(self.headshot.name).startswith('http'):
                return self.headshot.name
            # Otherwise, it's a file path, so use the .url property
            elif hasattr(self.headshot, 'url'):
                return self.headshot.url
        return ""

    @property
    def get_resume_url(self):
        if self.resume_file and hasattr(self.resume_file, 'name'):
            if str(self.resume_file.name).startswith('http'):
                return self.resume_file.name
            elif hasattr(self.resume_file, 'url'):
                return self.resume_file.url
        return "#"


class SocialLink(OrderedModel):
    label = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=80, blank=True)  # e.g. "bi bi-github"

    def __str__(self):
        return self.label

    class Meta(OrderedModel.Meta):
        pass


class SkillCategory(OrderedModel):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        pass


class Skill(OrderedModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=80)
    level = models.PositiveSmallIntegerField(default=0)  # 0–100
    order_with_respect_to = 'category'

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta(OrderedModel.Meta):
        pass


class ProjectCategory(Timestamped):
    name = models.CharField(max_length=50)  # e.g. "Photography", "Design"
    slug = models.SlugField(unique=True)  # e.g. "photography"

    def __str__(self):
        return self.name


class Project(Timestamped, OrderedModel):
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    tech_stack = models.CharField(max_length=240, blank=True)  # comma-separated tags
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image and hasattr(self.image, 'name'):
            if str(self.image.name).startswith('http'):
                return self.image.name
            elif hasattr(self.image, 'url'):
                return self.image.url
        return ""

    class Meta(OrderedModel.Meta):
        ordering = ["-featured", "-created_at"]


class Experience(OrderedModel):
    company = models.CharField(max_length=160)
    role = models.CharField(max_length=160)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.role} @ {self.company}"

    class Meta(OrderedModel.Meta):
        ordering = ["-start_date"]


class Education(OrderedModel):
    school = models.CharField(max_length=160)
    program = models.CharField(max_length=160)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.program} - {self.school}"

    class Meta(OrderedModel.Meta):
        ordering = ["-start_date"]


class Certification(OrderedModel):
    name = models.CharField(max_length=160)
    issuer = models.CharField(max_length=160, blank=True)
    issue_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    class Meta(OrderedModel.Meta):
        ordering = ["-issue_date", "name"]


class Service(OrderedModel):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=80, blank=True)  # e.g., "bi bi-code-slash"
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image and hasattr(self.image, 'name'):
            # Check if the raw value is a full URL
            if str(self.image.name).startswith('http'):
                return self.image.name
            # Otherwise, it's a file path, so use the .url property
            elif hasattr(self.image, 'url'):
                return self.image.url
        return ""

    class Meta(OrderedModel.Meta):
        pass


class ContactMessage(Timestamped):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"


class Stat(OrderedModel):
    label = models.CharField(max_length=50)  # e.g. "Happy Clients"
    count = models.IntegerField()  # e.g. 50
    icon_class = models.CharField(max_length=50, blank=True)  # e.g. "bi bi-emoji-smile"

    class Meta(OrderedModel.Meta):
        pass


class Award(OrderedModel):
    title = models.CharField(max_length=160)
    issuer = models.CharField(max_length=160)
    year = models.CharField(max_length=4)
    description = models.TextField(blank=True)

    class Meta(OrderedModel.Meta):
        ordering = ['-year']
