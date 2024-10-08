from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentsForm
from .models import Students
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
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
    students = Students.objects.all()
    return render(request, 'student/index.html', {'students': students, 'student': True, 'section': 'student'})

def student_create(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST)
        if form.is_valid():
            form.save() # Simpan data mahasiswa ke database
            messages.success(request, 'Mahasiswa berhasil dibuat!') # Pesan sukses
        return redirect('student_index') 
    else:
        form = StudentsForm()
        return render(request, 'student/create.html', {'form': form, 'student': True, 'section': 'student'})
    
def student_update(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    if request.method == 'POST':
        form = StudentsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data mahasiswa berhasil diubah!')
            return redirect('student_index')
    else:
        form = StudentsForm(instance=student)
    return render(request, 'student/update.html', {'form': form, 'student': student, 'section': 'student'})

# DELETE Mahasiswa
def student_delete(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    student.delete()
    messages.success(request, 'Data mahasiswa berhasil dihapus')
    return JsonResponse({'success': True})

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