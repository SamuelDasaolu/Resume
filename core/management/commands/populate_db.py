import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from core.models import (
    Profile, SocialLink, SkillCategory, Skill, ProjectCategory, Project,
    Experience, Education, Certification, Service, Stat, Award
)


class Command(BaseCommand):
    help = 'Populates the database with a rich set of dummy data using direct image URLs'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate the database with comprehensive dummy data...')
        fake = Faker()

        # --- 0. CLEAN UP EXISTING DATA ---
        self.stdout.write('Clearing old data...')
        Profile.objects.all().delete()
        SocialLink.objects.all().delete()
        SkillCategory.objects.all().delete()
        Project.objects.all().delete()
        ProjectCategory.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()
        Certification.objects.all().delete()
        Service.objects.all().delete()
        Stat.objects.all().delete()
        Award.objects.all().delete()

        # --- Image URLs ---
        # Using a predefined list of reliable URLs to avoid placeholder service issues
        profile_image_url = "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=400"
        project_image_urls = [
            "https://images.pexels.com/photos/577585/pexels-photo-577585.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/1181244/pexels-photo-1181244.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "https://images.pexels.com/photos/1181298/pexels-photo-1181298.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
        ]
        service_image_urls = random.sample(project_image_urls, 5) # Reuse for services

        # --- 1. PROFILE (Single Entry) ---
        self.stdout.write('Creating Profile...')
        profile_name = fake.name()
        Profile.objects.create(
            full_name=profile_name,
            title=f"{fake.job()} & {fake.job()}",
            summary=fake.text(max_nb_chars=1000),
            email=fake.email(),
            location=f"{fake.city()}, {fake.country()}",
            headshot=profile_image_url,
            resume_file="https://example.com/resume.pdf"
        )

        # --- 2. SOCIAL LINKS (At least 5) ---
        self.stdout.write('Creating Social Links...')
        socials = [
            ('GitHub', 'bi bi-github'), ('LinkedIn', 'bi bi-linkedin'),
            ('Twitter', 'bi bi-twitter'), ('Facebook', 'bi bi-facebook'),
            ('Instagram', 'bi bi-instagram'), ('Stack Overflow', 'bi bi-stack-overflow')
        ]
        for label, icon in random.sample(socials, 5):
            SocialLink.objects.create(
                label=label,
                url=f"https://{label.lower().replace(' ', '')}.com/{fake.user_name()}",
                icon_class=icon
            )

        # --- 3. SKILL CATEGORIES & SKILLS (Multiple Categories, >=5 Skills each) ---
        self.stdout.write('Creating Skills...')
        skill_categories = ['Frontend', 'Backend', 'Databases', 'DevOps', 'Cloud Platforms']
        for cat_name in skill_categories:
            category = SkillCategory.objects.create(name=cat_name)
            for _ in range(random.randint(5, 8)):
                Skill.objects.create(
                    category=category,
                    name=fake.word().capitalize(),
                    level=random.randint(70, 98)
                )

        # --- 4. PROJECT CATEGORIES & PROJECTS (Multiple Categories, >=5 Projects total) ---
        self.stdout.write('Creating Projects...')
        project_categories = ['Web Development', 'Mobile App', 'Data Science', 'Automation', 'Cloud Infrastructure']
        created_projects = 0
        for cat_name in project_categories:
            if created_projects >= 5: break
            slug = slugify(cat_name)
            category, _ = ProjectCategory.objects.get_or_create(name=cat_name, slug=slug)
            for i in range(random.randint(1, 2)):
                if created_projects >= 5: break
                title = f"{fake.bs().title()} {cat_name} Project"
                Project.objects.create(
                    category=category,
                    title=title,
                    slug=slugify(title),
                    description=fake.paragraph(nb_sentences=8),
                    tech_stack=", ".join(fake.words(nb=random.randint(4, 7))),
                    repo_url=f"https://github.com/{fake.user_name()}/{slugify(title)}",
                    live_url=fake.url(),
                    featured=random.choice([True, False, False]),
                    image=project_image_urls[created_projects]
                )
                created_projects += 1

        # --- 5. EXPERIENCE (At least 5) ---
        self.stdout.write('Creating Experience...')
        for _ in range(5):
            Experience.objects.create(
                company=fake.company(),
                role=fake.job(),
                start_date=fake.date_between(start_date='-10y', end_date='-1y'),
                end_date=fake.date_between(start_date='-1y', end_date='today') if random.choice([True, False]) else None,
                location=f"{fake.city()}, {fake.country()}",
                description=fake.text(max_nb_chars=500)
            )

        # --- 6. EDUCATION (At least 5) ---
        self.stdout.write('Creating Education...')
        for _ in range(5):
            Education.objects.create(
                school=f"{fake.city().title()} University",
                program=f"{random.choice(['B.S.', 'M.S.'])} in {fake.word().capitalize()} Science",
                start_date=fake.date_between(start_date='-12y', end_date='-6y'),
                end_date=fake.date_between(start_date='-5y', end_date='-1y'),
                description=fake.sentence()
            )

        # --- 7. CERTIFICATIONS (At least 5) ---
        self.stdout.write('Creating Certifications...')
        for _ in range(5):
            Certification.objects.create(
                name=f"Certified {fake.job()}",
                issuer=f"{fake.company()} Institute",
                issue_date=fake.date_this_decade(),
                url=fake.url()
            )

        # --- 8. SERVICES (At least 5) ---
        self.stdout.write('Creating Services...')
        service_icons = ['bi bi-briefcase', 'bi bi-card-checklist', 'bi bi-bar-chart', 'bi bi-binoculars', 'bi bi-brightness-high', 'bi bi-calendar4-week']
        for i in range(5):
            title = fake.catch_phrase()
            Service.objects.create(
                title=title,
                slug=slugify(title),
                short_description=fake.sentence(nb_words=10),
                description=fake.text(max_nb_chars=400),
                icon_class=random.choice(service_icons),
                featured=random.choice([True, False]),
                image=service_image_urls[i]
            )

        # --- 9. STATS (At least 5) ---
        self.stdout.write('Creating Stats...')
        stats_data = [
            ('Happy Clients', 'bi bi-emoji-smile'), ('Projects Completed', 'bi bi-journal-richtext'),
            ('Hours of Support', 'bi bi-headset'), ('Awards Won', 'bi bi-award'),
            ('Cups of Coffee', 'bi bi-cup-hot'), ('Lines of Code', 'bi bi-file-code')
        ]
        for label, icon in random.sample(stats_data, 5):
            Stat.objects.create(
                label=label,
                count=random.randint(20, 1000),
                icon_class=icon
            )

        # --- 10. AWARDS (At least 5) ---
        self.stdout.write('Creating Awards...')
        for _ in range(5):
            Award.objects.create(
                title=f"{fake.word().capitalize()} Award for Excellence in {fake.word()}",
                issuer=f"{fake.company()} Foundation",
                year=str(fake.year()),
                description=fake.sentence()
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with a rich set of dummy data.'))
