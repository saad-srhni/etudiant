from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Classroom, Attendance
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ClassroomForm, StudentForm, StudentAttendanceForm
from django.contrib import messages
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import calendar
from calendar import monthrange
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from io import BytesIO

@login_required
def student_list(request):
    students = Student.objects.all()
    classrooms = Classroom.objects.all()

    # Retrieve filter values
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')
    email = request.GET.get('email', '')
    telephone = request.GET.get('telephone', '')
    roll_number = request.GET.get('roll_number', '')
    classroom = request.GET.get('classroom', '')  # classroom = classroom ID

    # Apply filters
    if first_name:
        students = students.filter(first_name__icontains=first_name)
    if last_name:
        students = students.filter(last_name__icontains=last_name)
    if email:
        students = students.filter(email__icontains=email)
    if telephone:
        students = students.filter(telephone__icontains=telephone)
    if roll_number:
        students = students.filter(roll_number__icontains=roll_number)
    if classroom:
        students = students.filter(classrooms__id=classroom).distinct()

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'request': request,
        'classrooms': classrooms,
        'selected_classroom': classroom,
    })

@login_required
def create_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('classroom_list')
    else:
        form = ClassroomForm()
    return render(request, 'create_classroom.html', {'form': form})

@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            form.save_m2m()  # Save many-to-many data
            messages.success(request, "Student created successfully.")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'create_student.html', {'form': form})

@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            form.save_m2m()  # Save many-to-many data
            messages.success(request, "Student updated successfully.")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'create_student.html', {'form': form})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted.")
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {'student': student})

@login_required
def classroom_list(request):
    search = request.GET.get('search', '')
    classrooms = Classroom.objects.all()

    if search:
        classrooms = classrooms.filter(
            Q(name__icontains=search) |
            Q(subject__icontains=search)
        )

    paginator = Paginator(classrooms, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'classroom_list.html', {
        'page_obj': page_obj,
        'search': search,
    })

@login_required
def update_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('classroom_list')
    else:
        form = ClassroomForm(instance=classroom)
    return render(request, 'create_classroom.html', {'form': form})

@login_required
def delete_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        classroom.delete()
        return redirect('classroom_list')
    return render(request, 'confirm_delete_classroom.html', {'classroom': classroom})

@login_required
def mark_attendance(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    students = Student.objects.filter(classrooms=classroom)

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
            Attendance.objects.update_or_create(
                student=student,
                date=date.today(),
                defaults={'status': status, 'classroom': classroom}
            )
        messages.success(request, "Attendance saved!")
        return redirect('student_list')

    return render(request, 'mark_attendance.html', {
        'classroom': classroom,
        'students': students,
        'today': date.today()
    })

@login_required
def view_student_classrooms(request, pk):
    student = get_object_or_404(Student, pk=pk)
    classrooms = student.classrooms.all()
    return render(request, 'student_classrooms.html', {
        'student': student,
        'classrooms': classrooms
    })

@login_required
def student_attendance_history(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')

    # Optional: filter by date
    date_filter = request.GET.get('date')
    if date_filter:
        attendance_records = attendance_records.filter(date=date_filter)

    return render(request, 'student_attendance_history.html', {
        'student': student,
        'records': attendance_records,
        'date_filter': date_filter
    })

@login_required
def mark_attendance_for_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = StudentAttendanceForm(request.POST, student=student)
        print(form.errors)
        if form.is_valid():
            classroom = form.cleaned_data['classroom']
            status = form.cleaned_data['status']

            Attendance.objects.update_or_create(
                student=student,
                classroom=classroom,
                defaults={'status': status}
            )
            messages.success(request, "✅ Attendance saved successfully!")
            return redirect('student_list')
    else:
        form = StudentAttendanceForm(student=student)

    return render(request, 'mark_attendance_student.html', {
        'form': form,
        'student': student
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_list')  # or home
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


@login_required
def attendance_calendar(request, student_id, year=None, month=None):
    student = get_object_or_404(Student, pk=student_id)

    today = date.today()
    year = year or today.year
    month = month or today.month

    first_day, num_days = monthrange(year, month)
    month_days = [date(year, month, day) for day in range(1, num_days + 1)]

    attendance_data = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    )

    attendance_dict = {att.date: att.status for att in attendance_data}

    calendar_data = []
    for day in month_days:
        status = attendance_dict.get(day, 'nodata')  # present/absent/nodata
        calendar_data.append({'date': day, 'status': status})

    context = {
        'student': student,
        'calendar_data': calendar_data,
        'month': month,
        'year': year,
        'month_name': calendar.month_name[month],
    }
    return render(request, 'calendar_view.html', context)

@login_required
def export_attendance_pdf(request):
    classroom_id = request.GET.get("classroom")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    students = Student.objects.all()
    if classroom_id:
        students = students.filter(classrooms__id=classroom_id).distinct()

    attendance_qs = Attendance.objects.filter(student__in=students)
    if classroom_id:
        attendance_qs = attendance_qs.filter(classroom_id=classroom_id)
    if start_date:
        attendance_qs = attendance_qs.filter(date__gte=start_date)
    if end_date:
        attendance_qs = attendance_qs.filter(date__lte=end_date)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, "📄 Attendance Report")
    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Classroom ID: {classroom_id or 'All'}")
    y -= 20
    p.drawString(50, y, f"Date range: {start_date or 'All'} to {end_date or 'All'}")
    y -= 30

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Student")
    p.drawString(200, y, "Classroom")
    p.drawString(350, y, "Date")
    p.drawString(450, y, "Status")
    y -= 20

    p.setFont("Helvetica", 10)
    for att in attendance_qs.order_by('date'):
        if y < 60:
            p.showPage()
            y = height - 50
        p.drawString(50, y, f"{att.student.first_name} {att.student.last_name}")
        p.drawString(200, y, att.classroom.name)
        p.drawString(350, y, att.date.strftime("%Y-%m-%d"))
        p.drawString(450, y, att.status)
        y -= 15

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")

