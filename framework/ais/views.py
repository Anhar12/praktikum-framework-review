from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentsForm
from .models import Students
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from rest_framework import viewsets
from .serializers import StudentsSerializer
import requests

# Create your views here.
class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

def homepage(request):
    context = {
        'section': 'home'
    }
    return render(request, 'homepage/index.html', context)

def about(request):
    context = {
        'section': 'about'
    }
    return render(request, 'homepage/about.html', context)

def student_index(request):
    query = request.GET.get('q')
    if query:
        response = requests.get(f'http://127.0.0.1:8000/api/students/?search={query}', verify=False)
    else:
        response = requests.get('http://127.0.0.1:8000/api/students/', verify=False)
    
    if response.status_code == 200:
        students = response.json()
    else:
        students = []
    return render(request, 'student/index.html', {'students': Students.objects.all(), 'query': query})

def student_create(request):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'nim': request.POST.get('nim'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'year': request.POST.get('year'),
            'teacher': request.POST.get('teacher'), 
        }

        response = requests.post('http://127.0.0.1:8000/api/students/', data=form_data, verify=False)
        if response.status_code == 201:
            messages.success(request, 'Mahasiswa berhasil dibuat!')
            return redirect('student_index')
        else:
            messages.error(request, 'Gagal membuat mahasiswa: ' + response.text)
    else:
        form_data = {}
    return render(request, 'student/create.html', {'form': StudentsForm()})
    
def student_update(request, student_id):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'nim': request.POST.get('nim'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'year': request.POST.get('year'),
            'teacher': request.POST.get('teacher'),
        }
        response = requests.put(f'http://127.0.0.1:8000/api/students/{student_id}/', data=form_data, verify=False)
        if response.status_code == 200:
            messages.success(request, 'Data mahasiswa berhasil diubah!')
            return redirect('student_index')
        else:
            messages.error(request, 'Gagal mengubah mahasiswa: ' + response.text)
    else:
        response = requests.get(f'http://127.0.0.1:8000/api/students/{student_id}/', verify=False)
        if response.status_code == 200:
            student = response.json() 
        else:
            return HttpResponseForbidden("Data mahasiswa tidak ditemukan.")
    return render(request, 'student/update.html', {'form': StudentsForm(initial=student), 'student': student})

# DELETE Mahasiswa
def student_delete(request, student_id):
    if request.method == 'POST':
        response = requests.delete(f'http://127.0.0.1:8000/api/students/{student_id}/', verify=False)
        if response.status_code == 204: 
            messages.success(request, 'Data mahasiswa berhasil dihapus')
            return JsonResponse({'success': True})
        else:
            messages.error(request, 'Gagal menghapus mahasiswa: ' + response.text)
            return JsonResponse({'success': False})
    else:
        return HttpResponseForbidden("Metode tidak diizinkan.")

def student_index(request):
    query = request.GET.get('q')
    students = Students.objects.all()
    if query:
        students = Students.objects.filter(
            Q(name__icontains=query) |
            Q(nim__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )
    else:
        students = Students.objects.all()
    return render(request, 'student/index.html', {'students': students, 'query': query, 'section': 'student'})

@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Student').exists():
        return redirect('dashboard_student')
    elif user.groups.filter(name='Teacher').exists():
        return redirect('dashboard_teacher')
    return HttpResponseForbidden("You do not have permission to access this page.")

@group_required('Admin')
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@group_required('Student')
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@group_required('Teacher')
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')