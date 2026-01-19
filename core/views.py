from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .forms import ContactForm
from .models import (
    Profile, SocialLink, SkillCategory, Project, ProjectCategory,
    Experience, Education, Certification, Service, Stat, Award, ContactMessage
)


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = ContactForm()

    # Get the most recently updated profile
    profile = Profile.objects.latest('updated_at') if Profile.objects.exists() else None

    context = {
        'profile': profile,
        'socials': SocialLink.objects.all(),
        'skill_categories': SkillCategory.objects.prefetch_related('skills').all(),

        # Portfolio Section
        # select_related boosts performance by fetching the category in the same query
        'projects': Project.objects.select_related('category').all(),
        'project_categories': ProjectCategory.objects.all(),  # For the filter buttons

        # Resume Section
        'experiences': Experience.objects.all(),
        'education_list': Education.objects.all(),
        'certifications': Certification.objects.all(),
        'awards': Award.objects.all(),

        # Other Sections
        'stats': Stat.objects.all(),
        'services': Service.objects.all(),
        'form': form,
    }
    return render(request, template_name='index_snapfolio.html', context=context)


def preview(request):
    """Static preview for testing templates without data."""
    return render(request, 'index_snapfolio.html', {})


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio_detail_snapfolio.html'


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail_snapfolio.html'
