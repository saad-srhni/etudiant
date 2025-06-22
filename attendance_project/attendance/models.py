from django.db import models
from datetime import date


class Classroom(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    telephone = models.CharField(max_length=20)
    roll_number = models.CharField(max_length=20, unique=True)
    classrooms = models.ManyToManyField('Classroom', related_name='students')  # changed here

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)  # ✅ This sets default to today's date
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'classroom', 'date')  # ✅ Prevent duplicates

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

