from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Add these imports for admin functionality
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Add these imports for admin functionality
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Project, Skill, BlogPost, Certification, About

# --- Main Page Views ---

def home_view(request):
    """The main landing page view (Hero and teasers)."""
    # Later, you will fetch teaser data here.
    return render(request, 'portfolio/index.html')

def about_view(request):
    """The dedicated About Me and Skills page."""
    # Later, you can pass specific profile data here.
    return render(request, 'portfolio/about.html')

def projects_view(request):
    """The dedicated Projects list page."""
    # Later, you will fetch all projects here.
    return render(request, 'portfolio/projects.html')

def blogs_view(request):
    """The dedicated Blogs index page."""
    # Later, you will fetch blog previews here.
    return render(request, 'portfolio/blogs.html')

# def contact_view(request):
#     """The dedicated Contact form page (handles GET and POST)."""
#     if request.method == 'POST':
#         # NOTE: This is a simplified placeholder for now.
#         # In a real application, you would:
#         # 1. Validate the form data.
#         # 2. Save the message to the database or send an email.
        
#         # For now, let's just confirm receipt (do not use alert() in production!)
#         # We will implement a proper success message later.
        
#         # Simulating successful form submission:
#         # print(f"Received message from {request.POST.get('name')}")
#         return redirect('portfolio:contact') # Redirect to prevent resubmission
        
#     return render(request, 'portfolio/contact.html')

# --- Detail Views (Placeholders) ---

def project_details_view(request, pk):
    """Detail page for a specific project."""
    # Logic to fetch project by PK
    return render(request, 'portfolio/project_details.html', {'project_id': pk})

def blog_details_view(request, pk):
    """Detail page for a specific blog post."""
    # Logic to fetch blog post by PK
    return HttpResponse(f"Blog Post Details for ID: {pk}") 
    # Replace HttpResponse with render(request, 'portfolio/blog_details.html', ...) later
    

def contact_view(request):
    if request.method == 'POST':
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                name = data.get('name')
                email = data.get('email')
                subject = data.get('subject')
                message = data.get('message')
                
                # Validate required fields
                if not all([name, email, subject, message]):
                    return JsonResponse({
                        'success': False,
                        'message': 'Please fill in all required fields.'
                    }, status=400)
                
                # Email to you (the site owner)
                owner_subject = f"Portfolio Contact: {subject}"
                owner_message = f"""
                New contact form submission:

                Name: {name}
                Email: {email}
                Subject: {subject}

                Message:
                {message}

                ---
                Sent from your portfolio website.
                """
                
                send_mail(
                    owner_subject,
                    owner_message,
                    email,  
                    ['jonasmwansa@dev.com'], 
                    fail_silently=False,
                )
                
                # Optional: Send confirmation email to the user
                user_subject = "Thank you for contacting Jonas"
                user_message = f"""
                Hi {name},

                Thank you for reaching out! I've received your message and will get back to you as soon as possible.

                Here's a copy of your message:
                Subject: {subject}
                Message: {message}

                Best regards,
                Jonas Mwansa
                Applications Developer

                ---
                This is an automated response.
                """
                
                send_mail(
                    user_subject,
                    user_message,
                    'noreply@jonasmwansa.dev',  # From email
                    [email],  # User's email
                    fail_silently=False,
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Your message has been sent successfully! I will get back to you soon.'
                })
                
            except BadHeaderError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid header found. Please try again.'
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'There was an error sending your message. Please try again later.'
                }, status=500)
        
        # Regular form submission (fallback)
        else:
            # ... keep your existing non-AJAX code here as fallback
            pass
    
    return render(request, 'portfolio/contact.html')

# =============================================================================
# ADMIN DASHBOARD VIEWS - ADD THESE TO YOUR EXISTING VIEWS
# =============================================================================


def admin_login(request):
    """Custom admin login with AJAX support"""
    if request.user.is_authenticated:
        return redirect('portfolio:admin-dashboard')

    next_url = request.GET.get('next', '')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        # AJAX request?
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "status": "success",
                    "message": "Welcome to your portfolio dashboard!",
                    "redirect_url": request.POST.get("next") or "/dashboard/"
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid username or password"
                })

        # Normal fallback (non-AJAX)
        if user is not None:
            login(request, user)
            return redirect(request.POST.get("next") or 'portfolio:admin-dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "admin/login.html", {"next": next_url})



def admin_logout(request):
    """Custom admin logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('portfolio:home')

@login_required
def admin_dashboard(request):
    """Admin dashboard overview with meaningful metrics"""
    
    # Basic counts
    projects_count = Project.objects.count()
    blog_count = BlogPost.objects.count()
    skills_count = Skill.objects.count()
    certifications_count = Certification.objects.count()
    
    # Initialize variables with default values
    last_project = None
    days_since_update = 999
    last_update_date = timezone.now()
    featured_projects_count = projects_count  # Fallback
    skills_categories_count = 1  # Fallback
    about_complete = False
    skill_categories = []
    
    # Handle missing fields gracefully
    try:
        featured_projects_count = Project.objects.filter(is_featured=True).count()
    except:
        featured_projects_count = projects_count  # Fallback
    
    try:
        skills_categories_count = Skill.objects.values('category').distinct().count()
    except:
        skills_categories_count = 1  # Fallback
    
    # Content health calculations
    total_sections = 5  # projects, blog, skills, certs, about
    completed_sections = 0
    if projects_count >= 1: completed_sections += 1
    if blog_count >= 1: completed_sections += 1
    if skills_count >= 1: completed_sections += 1
    if certifications_count >= 1: completed_sections += 1
    
    # Check About completeness
    try:
        from .models import About  # Import here to avoid circular imports
        about_exists = About.objects.exists()
        if about_exists:
            about = About.objects.first()
            about_complete = about.is_complete
        else:
            about_complete = False
    except:
        about_complete = False
    
    # Days since last update
    try:
        last_project = Project.objects.order_by('-updated_at').first()
        if last_project:
            days_since_update = (timezone.now() - last_project.updated_at).days
            last_update_date = last_project.updated_at
        else:
            days_since_update = 999
            last_update_date = timezone.now()
    except:
        days_since_update = 999
        last_update_date = timezone.now()
    
    # Skill categories with counts
    category_colors = ['#4361ee', '#4cc9f0', '#f72585', '#7209b7', '#3a0ca3', '#4361ee']
    
    try:
        for i, (category_value, category_name) in enumerate(Skill.CATEGORY_CHOICES):
            count = Skill.objects.filter(category=category_value).count()
            if count > 0:
                skill_categories.append({
                    'name': category_name,
                    'count': count,
                    'color': category_colors[i % len(category_colors)]
                })
    except:
        # If categories don't exist yet
        skill_categories = []
    
    # Portfolio score (0-100)
    portfolio_score = min(100, (
        (min(projects_count, 5) / 5 * 25) +  # Projects weight: 25%
        (min(blog_count, 3) / 3 * 20) +      # Blog weight: 20%
        (min(skills_count, 10) / 10 * 20) +  # Skills weight: 20%
        (min(certifications_count, 3) / 3 * 15) +  # Certs weight: 15%
        (1 if about_complete else 0) * 20    # About weight: 20%
    ))
    
    # Get recent projects
    recent_projects = Project.objects.all().order_by('-updated_at')[:5]
    
    context = {
        # Basic counts
        'projects_count': projects_count,
        'blog_count': blog_count,
        'skills_count': skills_count,
        'certifications_count': certifications_count,
        
        # Advanced metrics
        'featured_projects_count': featured_projects_count,
        'skills_categories_count': skills_categories_count,
        'completed_sections': completed_sections,
        'total_sections': total_sections,
        'days_since_update': days_since_update,
        'about_complete': about_complete,
        'skill_categories': skill_categories,
        'total_content_items': projects_count + blog_count + skills_count + certifications_count,
        'featured_items_count': featured_projects_count,
        'portfolio_score': int(portfolio_score),
        'last_update_date': last_update_date,
        
        # Recent activity
        'recent_projects': recent_projects,
        'recent_posts': BlogPost.objects.all().order_by('-published_date')[:3],
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
def manage_projects(request):
    """Manage projects page"""
    try:
        projects = Project.objects.all().order_by('-created_at')
    except:
        projects = []
    return render(request, 'admin/manage_projects.html', {'projects': projects})

@login_required
def manage_skills(request):
    """Manage skills page"""
    try:
        skills = Skill.objects.all().order_by('category', 'name')
    except:
        skills = []
    return render(request, 'admin/manage_skills.html', {'skills': skills})

@login_required
def manage_blog(request):
    """Manage blog posts page"""
    try:
        posts = BlogPost.objects.all().order_by('-published_date')
    except:
        posts = []
    return render(request, 'admin/manage_blog.html', {'posts': posts})

@login_required
def manage_about(request):
    """Manage about me page"""
    return render(request, 'admin/manage_about.html')

@login_required
def manage_certifications(request):
    """Manage certifications page"""
    try:
        certifications = Certification.objects.all().order_by('-issue_date')
    except:
        certifications = []
    return render(request, 'admin/manage_certifications.html', {'certifications': certifications})

