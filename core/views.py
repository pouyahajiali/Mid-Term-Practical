from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, TextbookForm
from .models import Textbook
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def home_page(request):
    course_codes = Textbook.objects.values_list('course_code', flat=True).distinct()
    print(course_codes)
    return render(request, 'home.html', {
        'course_codes': course_codes,
    })


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('my_textbooks')
        else:
            messages.error(request, 'Wrong username or password.')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'You logged out.')
    return redirect('login')


def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def add_textbook_page(request):
    if request.method == 'POST':
        form = TextbookForm(request.POST)
        if form.is_valid():
            textbook = form.save(commit=False)
            textbook.owner = request.user
            textbook.save()
            messages.success(request, 'successfully! added')
            return redirect('my_textbooks')
        else:
            print(form.errors)
            messages.error(request, 'Fix the errors.')
    else:
        form = TextbookForm()

    return render(request, 'add_textbook.html', {'form': form})


def my_textbooks_page(request):
    textbooks = Textbook.objects.filter(is_available=True)
    return render(request, 'my_textbooks.html', {'textbooks': textbooks})


@login_required
def textbook_list_by_course_page(request, course_code):
    textbooks = Textbook.objects.filter(course_code=course_code, is_available=True)

    if not textbooks.exists():
        messages.info(request, f"No textbooks for course {course_code}.")

    return render(request, 'textbook_list.html', {
        'course_code': course_code,
        'textbooks': textbooks
    })


@login_required
def delete_textbook_page(request, textbook_id):
    textbook = get_object_or_404(Textbook, id=textbook_id)

    if textbook.owner != request.user:
        messages.error(request, 'You do not have permission to delete this textbook.')
        return redirect('my_textbooks')

    textbook.delete()
    messages.success(request, 'Textbook deleted successfully.')

    return redirect('my_textbooks')