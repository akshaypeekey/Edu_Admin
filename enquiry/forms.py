from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class EnquiryForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = ['student_name', 'address', 'qualification', 'college', 'course', 'batch_code', 'contact',
                  'email', 'enquiry_date', 'followup_date', 'status', 'counsellor_name', 'notes']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch_code': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'enquiry_date': forms.DateInput(format=('%y/%m/%d'),attrs={'class': 'form-control', 'type': 'date'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'counsellor_name': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean(self):
            pass


class EnquiryUpdateForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = ['student_name', 'address', 'qualification', 'college', 'course', 'batch_code', 'contact', 'email', 'enquiry_date', 'followup_date', 'status', 'counsellor_name', 'notes']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch_code': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'enquiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'followup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'counsellor_name': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_duration']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_duration': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass


class CounsellorCreateForm(ModelForm):
    class Meta:
        model = Counsellor
        fields = ['counsellor_name', 'counsellor_phone', 'counsellor_email']
        widgets = {
            'counsellor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'counsellor_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'counsellor_email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass

class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_code', 'course', 'batch_date', 'batch_status']

        widgets = {
            'batch_code': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch_date': forms.DateInput(format=('%y/%m/%d'),attrs={'class': 'form-control', 'type': 'date'}),
            'batch_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass


class CourseUpdateForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_duration']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_duration': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass


class BatchUpdateForm(ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_code', 'course', 'batch_date', 'batch_status']
        widgets={
            'batch_code': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'batch_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'batch_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass


class FollowUpViewForm(ModelForm):
    class Meta:
        model = Enquiry
        fields = ['followup_date']
        widgets = {
            'followup_date': forms.DateInput(format=('%y/%m/%d'),attrs={'class': 'form-control', 'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('followup_date')
        qs = Enquiry.objects.filter(followup_date=date,status='1')
        if qs:
            print("Found")
        else:
            msg = "No Follow Ups on selected date"
            self.add_error("followup_date",msg)
            print("error")


class NewAdmissionForm(ModelForm):
    class Meta:
        model = Admission
        exclude = ['date']
        widgets = {
            'admission_no': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'batch_code': forms.HiddenInput(),
            'enquiry_id': forms.HiddenInput(),
            'course_fee': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        exclude = ['payment_date',]
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_no': forms.HiddenInput(),
            'enquiry_id': forms.HiddenInput(),
        }

    def clean(self):
        pass


class StudentPayForm(ModelForm):
    class Meta:
        model = Admission
        fields = ['admission_no']
        widgets = {
            'admission_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        pass


class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
        }