from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

from .models import Profile, SocialLink, SkillCategory, Project, Experience, Education, Certification, Service

def index(request):
    profile = Profile.objects.order_by('-updated_at').first()
    context = {
        'profile': profile,
        'socials': SocialLink.objects.all(),
        'skill_categories': SkillCategory.objects.prefetch_related('skills').all(),
        'projects': Project.objects.all(),
        'experiences': Experience.objects.all(),
        'education_list': Education.objects.all(),
        'certifications': Certification.objects.all(),
        'services': Service.objects.all(),
    }
    return render(request, template_name='index_snapfolio.html', context=context)



def preview(request):
    # Render the Snapfolio preview without requiring DB models yet
    return render(request, 'index_snapfolio.html', {})


from django.shortcuts import get_object_or_404

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio_detail_snapfolio.html', {'project': project})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'service_detail_snapfolio.html', {'service': service})
