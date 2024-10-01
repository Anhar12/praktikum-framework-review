from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentsForm
from .models import Students

# Create your views here.
def homepage(request):
    context = {
        'home': True
    }
    return render(request, 'homepage/index.html', context)

def about(request):
    context = {
        'about': True
    }
    return render(request, 'homepage/about.html', context)

def student_index(request):
    students = Students.objects.all()
    return render(request, 'student/index.html', {'students': students, 'student': True})

def student_create(request):
    if request.method == 'POST':
        form = StudentsForm(request.POST)
        if form.is_valid():
            form.save() # Simpan data mahasiswa ke database
            messages.success(request, 'Mahasiswa berhasil dibuat!') # Pesan sukses
        return redirect('student_index') # Redirect ke halaman index mahasiswa
    else:
        form = StudentsForm()
        return render(request, 'student/create.html', {'form': form, 'student': True})