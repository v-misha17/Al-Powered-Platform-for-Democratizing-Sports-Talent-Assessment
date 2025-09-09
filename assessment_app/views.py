from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .models import SportAssessment
from .forms import VideoUploadForm
from .utils import process_video_assessment

def index(request):
    return render(request, 'assessment_app/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'assessment_app/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email', '')
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'assessment_app/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'assessment_app/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, 'Account created successfully')
        return redirect('index')
    
    return render(request, 'assessment_app/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('index')

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.user = request.user
            assessment.save()
            
            # Process video
            assessment, error = process_video_assessment(assessment)
            
            if assessment:
                return redirect('assessment_results', assessment_id=assessment.id)
            else:
                messages.error(request, error)
                return redirect('upload_video')
    else:
        form = VideoUploadForm()
    
    return render(request, 'assessment_app/upload.html', {'form': form})

@login_required
def assessment_results(request, assessment_id):
    assessment = get_object_or_404(SportAssessment, id=assessment_id, user=request.user)
    metrics = assessment.get_metrics()
    
    return render(request, 'assessment_app/results.html', {
        'assessment': assessment,
        'metrics': metrics
    })

@login_required
def assessment_history(request):
    assessments = SportAssessment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'assessment_app/history.html', {'assessments': assessments})