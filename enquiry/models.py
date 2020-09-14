from django.db import models
from datetime import date
import uuid


# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=50, unique=True)
    course_duration = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name


class Counsellor(models.Model):
    counsellor_name = models.CharField(max_length=50)
    counsellor_phone = models.CharField(max_length=13, null='True', blank='True')
    counsellor_email = models.EmailField(null='True', blank='True')

    def __str__(self):
        return self.counsellor_name


class Batch(models.Model):
    batch_code = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch_date = models.DateField(default=date.today())
    action = (
        ('1', 'Yet to begin'),
        ('2', 'Ongoing'),
        ('3', 'Completed')
    )
    batch_status = models.CharField(max_length=20, choices=action)

    def __str__(self):
        return self.batch_code


class Enquiry(models.Model):
    enquiry_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_name = models.CharField(max_length=30)
    address = models.TextField()
    qualification = models.CharField(max_length=20)
    college = models.CharField(max_length=30)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    batch_code = models.ForeignKey(Batch,on_delete=models.CASCADE)
    contact = models.IntegerField()
    email = models.EmailField(unique=True)
    enquiry_date = models.DateField(default=date.today())
    followup_date = models.DateField()
    action = (
        ('1','Call_Back'),
        ('2','Admitted'),
        ('3','Cancel')
    )
    status = models.CharField(max_length=20, choices=action)
    counsellor_name = models.ForeignKey(Counsellor,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.enquiry_id)


class Admission(models.Model):
    admission_no = models.CharField(max_length=30, editable='False')
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.CASCADE)
    batch_code = models.ForeignKey(Batch,on_delete=models.CASCADE)
    course_fee = models.IntegerField()
    date = models.DateField(default=date.today())
    notes = models.TextField(null='True', blank='True')

    def __str__(self):
        return self.admission_no


class Payment(models.Model):
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.CASCADE)
    admission_no = models.ForeignKey(Admission,on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField(default=date.today())


