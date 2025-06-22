from django import forms
from .models import Student, Classroom
from datetime import date


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'subject']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'subject': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
        }

class StudentForm(forms.ModelForm):
    classrooms = forms.ModelMultipleChoiceField(
        queryset=Classroom.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-1'}),
        required=False,
    )

    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'date_of_birth',
            'telephone', 'roll_number', 'classrooms'  # note the plural here
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'email': forms.EmailInput(attrs={'class': 'p-2 border rounded w-full'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'p-2 border rounded w-full'}),
            'telephone': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
            'roll_number': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
        }


class AttendanceForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=[('present', 'Present'), ('absent', 'Absent')],
                               widget=forms.RadioSelect())
    


class StudentAttendanceForm(forms.Form):
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.none(),  # we'll set this in the view
        label="Classroom",
        widget=forms.Select(attrs={'class': 'p-2 border rounded w-full'})
    )

    status = forms.ChoiceField(
        choices=[('present', 'Present'), ('absent', 'Absent')],
        label="Status",
        widget=forms.Select(attrs={'class': 'p-2 border rounded w-full'})
    )

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            self.fields['classroom'].queryset = student.classrooms.all()
