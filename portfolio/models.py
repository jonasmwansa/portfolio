# portfolio/models.py
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Project(models.Model):
    PROJECT_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    image = models.ImageField(upload_to='projects/')
    github_link = models.URLField(blank=True)
    live_demo_link = models.URLField(blank=True)
    
    # New fields for dashboard
    is_featured = models.BooleanField(default=False, help_text="Feature this project on the homepage")
    is_active = models.BooleanField(default=True, help_text="Show this project publicly")
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='draft')
    display_order = models.IntegerField(default=0, help_text="Order in which projects are displayed")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return self.title

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('tool', 'Tools & Technologies'),
        ('soft', 'Soft Skills'),
        ('ai_ml', 'AI & Machine Learning'),  # New category for AI focus
        ('cloud', 'Cloud & DevOps'),         # New category for Canonical focus
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(
        help_text="Proficiency level from 1-100",
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    icon_class = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    
    # New fields for dashboard
    is_featured = models.BooleanField(default=False, help_text="Show this skill prominently")
    years_experience = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=1.0,
        help_text="Years of experience with this skill"
    )
    last_used = models.DateField(default=timezone.now, help_text="When you last used this skill")
    
    class Meta:
        ordering = ['category', '-proficiency', 'name']
    
    def __str__(self):
        return self.name

class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    
    # New fields for dashboard
    is_verified = models.BooleanField(default=True)
    display_on_homepage = models.BooleanField(default=False, help_text="Show this certification on homepage")
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    featured_image = models.ImageField(upload_to='blog/')
    slug = models.SlugField(unique=True)
    
    # Enhanced fields for dashboard
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Feature this post on the homepage")
    read_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    view_count = models.IntegerField(default=0, help_text="Number of times this post has been viewed")
    
    published_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title

# New model for About section management
class About(models.Model):
    full_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    bio = models.TextField(help_text="Your professional bio/introduction")
    short_bio = models.TextField(max_length=300, help_text="Brief bio for homepage/cards")
    
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100)
    
    profile_image = models.ImageField(upload_to='about/', blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, help_text="Upload your CV/Resume")
    
    # Social links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Stats
    years_experience = models.IntegerField(default=0)
    projects_completed = models.IntegerField(default=0)
    happy_clients = models.IntegerField(default=0, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About"
    
    def __str__(self):
        return f"About - {self.full_name}"
    
    @property
    def is_complete(self):
        """Check if all essential about fields are filled"""
        essential_fields = [
            self.full_name, self.job_title, self.bio, 
            self.email, self.location, self.profile_image
        ]
        return all(essential_fields)

# New model for tracking portfolio analytics
class PortfolioAnalytics(models.Model):
    date = models.DateField(default=timezone.now)
    page_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    contact_form_submissions = models.IntegerField(default=0)
    resume_downloads = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Portfolio Analytics"
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics - {self.date}"

# New model for site settings
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Jonas Portfolio")
    site_description = models.TextField(default="Full Stack Developer & AI Enthusiast")
    maintenance_mode = models.BooleanField(default=False)
    google_analytics_id = models.CharField(max_length=20, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and SiteSettings.objects.exists():
            # Update the existing instance instead of creating new one
            existing = SiteSettings.objects.first()
            existing.site_name = self.site_name
            existing.site_description = self.site_description
            existing.maintenance_mode = self.maintenance_mode
            existing.google_analytics_id = self.google_analytics_id
            return existing.save(*args, **kwargs)
        return super().save(*args, **kwargs)