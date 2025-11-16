"""
portfolio/urls.py

URL configuration for portfolio application.

"""
from django.urls import path
from . import views

# Define the app namespace
app_name = 'portfolio'

urlpatterns = [
    # Main pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('projects/', views.projects_view, name='projects'),
    path('blogs/', views.blogs_view, name='blogs'),
    path('contact/', views.contact_view, name='contact'),
    
    # Detail pages (placeholders for now)
    path('projects/<int:pk>/', views.project_details_view, name='project_details'),
    path('blogs/<int:pk>/', views.blog_details_view, name='blog_details'),
    
    # Admin Dashboard URLs
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('dashboard/login/', views.admin_login, name='admin-login'),
    path('dashboard/logout/', views.admin_logout, name='admin-logout'),
    path('dashboard/projects/', views.manage_projects, name='manage-projects'),
    path('dashboard/skills/', views.manage_skills, name='manage-skills'),
    path('dashboard/blog/', views.manage_blog, name='manage-blog'),
    path('dashboard/about/', views.manage_about, name='manage-about'),
    path('dashboard/certifications/', views.manage_certifications, name='manage-certifications'),
]