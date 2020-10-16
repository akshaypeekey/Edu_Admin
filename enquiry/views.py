from urllib import request

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Enquiry
from .forms import *
# Create your views here.
from django.views.generic import *
from datetime import date


class Index(LoginRequiredMixin, TemplateView):
    model = Enquiry
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        from django.db.models import Count, Sum
        ytb_batch = Enquiry.objects.filter(batch_code__batch_status='1').values('batch_code__batch_code',
                                                                                'batch_code__batch_date',
                                                                                'batch_code__id').annotate(
            enq=Count('enquiry_id'))
        og_batch = Enquiry.objects.filter(batch_code__batch_status='2').values('batch_code__batch_code',
                                                                               'batch_code__batch_date',
                                                                               'batch_code__id').annotate(
            enq=Count('enquiry_id'))
        cd_batch = Enquiry.objects.filter(batch_code__batch_status='3').values('batch_code__batch_code',
                                                                               'batch_code__batch_date',
                                                                               'batch_code__id').annotate(
            enq=Count('enquiry_id'))
        tot_enq = Enquiry.objects.all().values('course__course_name').annotate(enq=Count('enquiry_id'))
        tot_adm = Enquiry.objects.filter(status='2').values('course__course_name').annotate(enq=Count('enquiry_id'))
        tot_call = Enquiry.objects.filter(status='1').values('course__course_name').annotate(enq=Count('enquiry_id'))
        tot_can = Enquiry.objects.filter(status='3').values('course__course_name').annotate(enq=Count('enquiry_id'))

        sum_enq = Enquiry.objects.all().count()
        sum_adm = Enquiry.objects.filter(status='2').count()
        sum_call = Enquiry.objects.filter(status='1').count()
        sum_can = Enquiry.objects.filter(status='3').count()

        total = Admission.objects.all().aggregate(total=Sum('course_fee'))
        received = Payment.objects.all().aggregate(total=Sum('amount'))

        received_values = received.values()
        values_list = list(received_values)
        received_value = (values_list[0])

        total_values = total.values()
        values_list1 = list(total_values)
        total_value = (values_list1[0])

        if (received_value == None) or (total_value == None):
            total = 0
            received = 0
            pending = 0
        else:
            pending = (int(total_value) - int(received_value))

        # Chart

        month_sum = (Payment.objects.annotate(m=ExtractMonth('payment_date')).values('m').annotate(
            total=Sum('amount')).order_by())
        # print(month_sum)

        context = {'ytb_batch': ytb_batch, 'og_batch': og_batch, 'cd_batch': cd_batch, 'tot_enq': tot_enq,
                   'tot_adm': tot_adm, 'tot_call': tot_call, 'tot_can': tot_can, 'sum_enq': sum_enq, 'sum_adm': sum_adm,
                   'sum_call': sum_call, 'sum_can': sum_can, 'total': total, 'received': received, 'pending': pending,
                   'month_sum': month_sum}

        return render(request, self.template_name, context)


class ReportUpdate(LoginRequiredMixin, TemplateView):
    model = Enquiry
    template_name = "enq/report.html"

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        ytb_batch = Enquiry.objects.filter(batch_code=id).values('batch_code__batch_code',
                                                                 'batch_code__batch_date').annotate(
            enq=Count('enquiry_id'))

        sum_enq = Enquiry.objects.filter(batch_code=id).count()
        sum_adm = Enquiry.objects.filter(batch_code=id, status='2').count()
        sum_call = Enquiry.objects.filter(batch_code=id, status='1').count()
        sum_can = Enquiry.objects.filter(batch_code=id, status='3').count()

        enq = Enquiry.objects.filter(batch_code=id).all()

        total = Admission.objects.filter(batch_code=id).aggregate(total=Sum('course_fee'))
        received = Payment.objects.filter(admission_no__batch_code=id).aggregate(total=Sum('amount'))

        received_values = received.values()
        values_list = list(received_values)
        received_value = (values_list[0])

        total_values = total.values()
        values_list1 = list(total_values)
        total_value = (values_list1[0])

        if (received_value == None) or (total_value == None):
            pending = 0
        else:
            pending = (int(total_value) - int(received_value))

        if sum_enq == 0:
            msg = "No Enquires Till Now"
        else:
            msg = ''

        context = {'ytb_batch': ytb_batch, 'enq': enq, 'sum_enq': sum_enq, 'sum_adm': sum_adm, 'sum_call': sum_call,
                   'sum_can': sum_can, 'total': total, 'received': received, 'pending': pending, 'msg': msg}

        # context={'tot_adm':tot_adm,'ytb_batch':ytb_batch,'tot_enq':tot_enq}

        return render(request, self.template_name, context)


@login_required
def createenq(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            enquiry_id = data.enquiry_id
            data.save()
            status = form.cleaned_data['status']
            if status == '2':
                messages.success(request, 'Enquiry successfully created. Please complete the Admission Process',
                                 'alert-success')
                return redirect('newadmission', pk=enquiry_id, )
            else:
                messages.success(request, 'Enquiry successfully created.', 'alert-success')
                return redirect('listenq')
        else:

            form = EnquiryForm()
            template_name = "enq/enq_form.html"
            context = {'form': form}
            messages.success(request, 'Data is not valid.', 'alert-danger')
            return render(request, template_name, context)
    else:
        form = EnquiryForm()
        template_name = "enq/enq_form.html"
        context = {'form': form}
        return render(request, template_name, context)


class EnquiryList(LoginRequiredMixin, ListView):
    model = Enquiry
    template_name = "enq/enq_list.html"


class AdmitionList(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "admission/admition_list.html"

    def get(self, request, *args, **kwargs):
        qs = Payment.objects.all().values('admission_no__admission_no', 'enquiry_id__student_name',
                                          'enquiry_id__course__course_name', 'enquiry_id__batch_code__batch_code',
                                          'enquiry_id__contact', 'admission_no__date', 'amount', 'enquiry_id',
                                          'enquiry_id__counsellor_name__counsellor_name').order_by('-payment_date')
        context = {'admit_list': qs}
        return render(request, self.template_name, context)


class AdmittedList(LoginRequiredMixin, ListView):
    model = Admission
    template_name = "admission/admitted_list.html"

    def get(self, request, *args, **kwargs):
        qs = Admission.objects.all().values('admission_no', 'enquiry_id__student_name', 'enquiry_id__contact',
                                            'enquiry_id__course__course_name', 'batch_code__batch_code',
                                            'course_fee', 'date', 'enquiry_id__enquiry_id')
        context = {'admit_list': qs}

        return render(request, self.template_name, context)


class ViewEnquiry(LoginRequiredMixin, DetailView):
    model = Enquiry
    template_name = "enq/enq_view.html"
    context_object_name = "details"


@login_required
def updateenq(request, pk):
    enq = Enquiry.objects.get(enquiry_id=pk)
    form = EnquiryUpdateForm(instance=enq)
    template_name = "enq/enq_update.html"
    context = {'form': form}
    if request.method == "POST":
        form = EnquiryUpdateForm(request.POST, instance=enq)
        if form.is_valid():
            data = form.save(commit=False)
            enquiry_id = data.enquiry_id
            data.save()
            admno = Admission.objects.filter(enquiry_id=pk)
            status = form.cleaned_data['status']
            if status == '2':
                if admno:
                    messages.success(request, 'Enquiry Details Updated.', 'alert-success')
                    return redirect('listadt')
                else:
                    messages.success(request, 'Enquiry Details Updated. Please Complete The Admission Process',
                                     'alert-success')
                    return redirect('newadmission', pk=enquiry_id)
            else:
                messages.success(request, 'Enquiry Details Updated.', 'alert-success')
                return redirect('listenq')
        else:
            messages.success(request, 'Data Is Not Valid.', 'alert-danger')
            return render(request, template_name, context)
    return render(request, template_name, context)


class DeleteEnquiry(LoginRequiredMixin, DeleteView):
    model = Enquiry
    template_name = "enq/enq_delete.html"
    success_url = reverse_lazy('listenq')


class FollowUp(LoginRequiredMixin, TemplateView):
    model = Enquiry
    template_name = "enq/enq-followups.html"

    def get(self, request, *args, **kwargs):
        enquiries = Enquiry.objects.filter(followup_date=date.today(), status='1')
        if enquiries:
            msg = ''
        else:
            msg = 'No Followup Today '

        context = {'enquiries': enquiries, 'msg': msg}
        return render(request, self.template_name, context)


class FollowUpDetail(LoginRequiredMixin, TemplateView):
    model = Enquiry
    form_class = EnquiryUpdateForm
    template_name = "enq/followupdetail.html"

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')

        qs = Enquiry.objects.get(enquiry_id=id)
        form = self.form_class(instance=qs)
        context = {'form': form, 'id': id}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Enquiry.objects.get(enquiry_id=id)
        form = self.form_class(request.POST, instance=qs)
        if form.is_valid():
            data = form.save(commit=False)
            enquiry_id = data.enquiry_id
            data.save()
            status = form.cleaned_data['status']
            if status == '2':
                return redirect('newadmission', pk=enquiry_id)
            else:
                return redirect('followup')
        else:
            form = self.form_class(request.POST)
            context = {'form': form}
            return render(request, self.template_name, context)


class ViewFollowUp(LoginRequiredMixin, TemplateView):
    model = Enquiry
    form_class = FollowUpViewForm
    template_name = "enq/viewfollowupsearch.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            dte = form.cleaned_data['followup_date']
            qs = Enquiry.objects.filter(followup_date=dte, status='1')
            if (qs):
                context = {'item': qs}
                template_name = "enq/viewfollowupall.html"
                return render(request, template_name, context)
            else:
                messages.success(request, 'No Followup On Selected Date', 'alert-primary')
                form = self.form_class(request.POST)
                context = {'form': form}
                return render(request, self.template_name, context)
        else:
            messages.success(request, 'No Followup On Selected Date', 'alert-primary')
            form = self.form_class(request.POST)
            context = {'form': form}
            return render(request, self.template_name, context)


class StudentInfoFollow(LoginRequiredMixin, TemplateView):
    model = Enquiry
    template_name = "enq/studentinfo_followup.html"

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Enquiry.objects.filter(enquiry_id=id)
        context = {'info': qs}
        return render(request, self.template_name, context)


class CounsellorCreation(LoginRequiredMixin, TemplateView):
    model = Counsellor
    form_class = CounsellorCreateForm
    template_name = "counsellor/counsellorcreation.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        counsellors = Counsellor.objects.all()
        context = {'form': form, 'counsellors': counsellors}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Counsellor Successfully Created', 'alert-success')
            return redirect('counselloradd')
        else:
            form = self.form_class(request.POST)
            counsellors = Counsellor.objects.all()
            context = {'form': form, 'counsellors': counsellors}
            messages.success(request, 'Invalid Data', 'alert-danger')
            return render(request, self.template_name, context)


class DeleteCounsellor(LoginRequiredMixin, DeleteView):
    model = Counsellor
    template_name = "counsellor/counsellordelete.html"
    success_url = reverse_lazy('counselloradd')


class CounsellorReport(LoginRequiredMixin, TemplateView):
    model = Counsellor
    template_name = "counsellor/counsellorreport.html"

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')

        data = Counsellor.objects.filter(id=id).values('counsellor_name')

        sum_enq = Enquiry.objects.filter(counsellor_name=id).count()
        sum_adm = Enquiry.objects.filter(counsellor_name=id, status='2').count()
        sum_call = Enquiry.objects.filter(counsellor_name=id, status='1').count()
        sum_can = Enquiry.objects.filter(counsellor_name=id, status='3').count()

        total = Admission.objects.filter(enquiry_id__counsellor_name=id).aggregate(total=Sum('course_fee'))
        received = Payment.objects.filter(enquiry_id__counsellor_name=id).aggregate(total=Sum('amount'))

        received_values = received.values()
        values_list = list(received_values)
        received_value = (values_list[0])

        total_values = total.values()
        values_list1 = list(total_values)
        total_value = (values_list1[0])

        if (received_value == None) or (total_value == None):
            pending = 0
        else:
            pending = (int(total_value) - int(received_value))

        if sum_enq == 0:
            msg = "No Enquires Attended By "
        else:
            msg = ''

        qs = Enquiry.objects.filter(counsellor_name=id).all()

        context = {'data': data, 'sum_enq': sum_enq, 'sum_adm': sum_adm, 'sum_call': sum_call, 'sum_can': sum_can,
                   'total': total, 'received': received, 'pending': pending, 'msg': msg, 'qs': qs}

        return render(request, self.template_name, context)


# Course creation

class CourseCreation(LoginRequiredMixin, TemplateView):
    model = Course
    form_class = CourseForm
    template_name = "course/coursecreation.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class
        courses = Course.objects.all()
        context = {'form': form, 'courses': courses}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                messages.success(request, 'Course Already Exists', 'alert-danger')
                return redirect('createcourse')
            messages.success(request, 'Course Successfully Created', 'alert-success')
            return redirect('createcourse')
        else:
            form = self.form_class(request.POST)
            context = {'form': form}
            messages.success(request, 'Invalid Data', 'alert-danger')
            return render(request, self.template_name, context)


class ViewCourse(LoginRequiredMixin, TemplateView):
    model = Course
    template_name = "course/viewcourse.html"

    def get(self, request, *args, **kwargs):
        qs = Course.objects.all()
        context = {'courselist': qs}
        return render(request, self.template_name, context)


class CourseUpdation(LoginRequiredMixin, TemplateView):
    model = Course
    form_class = CourseUpdateForm
    template_name = "course/courseupdate.html"

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Course.objects.get(id=id)
        form = self.form_class(instance=qs)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Course.objects.get(id=id)
        form = self.form_class(request.POST, instance=qs)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                messages.success(request, 'Course Already Exists', 'alert-danger')
                return redirect('courseupdate', pk=id)
            messages.success(request, 'Course Successfully Updated', 'alert-success')
            return redirect('createcourse')
        else:
            form = self.form_class(request.POST)
            context = {'form': form}
            messages.success(request, 'Invalid Data', 'alert-danger')
            return render(request, self.template_name, context)


class CourseDelete(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "course/coursedelete.html"
    success_url = reverse_lazy('createcourse')


class BatchCreation(LoginRequiredMixin, TemplateView):
    model = Batch
    template_name = "batch/batchcreate.html"
    form_class = BatchForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        batches = Batch.objects.all()
        context = {}
        context['form'] = form
        context['batches'] = batches
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                messages.success(request, 'Batch Code Already Exists', 'alert-danger')
                return redirect('createbatch')
            messages.success(request, 'New Batch Created', 'alert-success')
            return redirect('createbatch')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            messages.success(request, 'Incorrect Data', 'alert-danger')
            return render(request, self.template_name, context)


class BatchView(LoginRequiredMixin, TemplateView):
    model = Batch
    template_name = "batch/batchview.html"

    def get(self, request, *args, **kwargs):
        qs = Batch.objects.all()
        context = {'batch': qs}
        return render(request, self.template_name, context)


class BatchUpdate(LoginRequiredMixin, TemplateView):
    model = Batch
    template_name = "batch/batchupdate.html"
    form_class = BatchUpdateForm

    def get(self, request, *args, **kwargs):
        b_id = self.kwargs.get('pk')
        qs = Batch.objects.get(id=b_id)
        form = self.form_class(instance=qs)
        context = {}
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        b_id = self.kwargs.get('pk')
        qs = Batch.objects.get(id=b_id)
        form = self.form_class(request.POST, instance=qs)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                messages.success(request, 'Batch Code Already Exists', 'alert-danger')
                return redirect('updatebatch', pk=b_id)
            messages.success(request, 'Batch Updated', 'alert-success')
            return redirect('createbatch')
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            messages.success(request, 'Incorrect Data', 'alert-danger')
            return render(request, self.template_name, context)


class BatchDelete(LoginRequiredMixin, DeleteView):
    model = Batch
    template_name = "batch/batchdelete.html"
    success_url = reverse_lazy('createbatch')


class NewAdmission(LoginRequiredMixin, TemplateView):
    model = Admission
    template_name = "admission/new_admission.html"
    form_class = NewAdmissionForm

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Enquiry.objects.get(enquiry_id=id)
        name = qs.student_name
        batch_code = qs.batch_code

        course = qs.course
        last_admission = Admission.objects.filter(batch_code=batch_code).order_by('id').last()

        if not last_admission:
            admission_no = str(str(batch_code) + '-' + str(date.today().month).zfill(2)) + '-' + '100'
        else:
            admission_no = last_admission.admission_no
            admission_int = (admission_no[-3:])
            admission_int = int(admission_int) + 1
            admission_no = str(str(batch_code) + '-' + str(date.today().month).zfill(2)) + '-' + str(admission_int)

        form = self.form_class(initial={'enquiry_id': id, 'batch_code': batch_code, 'admission_no': admission_no})

        context = {'form': form, 'name': name, 'batch_code': batch_code, 'course': course}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            id = self.kwargs.get('pk')
            qs = Enquiry.objects.get(enquiry_id=id)
            enquiry_id = qs.enquiry_id
            qs.status = '2'
            qs.save()
            admission_no = form.cleaned_data['admission_no']
            form.save()
            return redirect('payment', pk=enquiry_id)
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)


class StudentPayment(LoginRequiredMixin, TemplateView):
    model = Payment
    template_name = "admission/payment.html"
    form_class = PaymentForm

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        qs = Admission.objects.get(enquiry_id=id)
        enqid = qs.enquiry_id
        fees = qs.course_fee

        from django.db.models import Sum
        qs2 = Payment.objects.filter(enquiry_id=id).values('amount').aggregate(total=Sum('amount'))

        if (qs2['total'] == None):
            remaining = fees
        else:
            remaining = fees - (qs2['total'])
        form = self.form_class(initial={'admission_no': qs, 'enquiry_id': enqid})
        context = {}
        context['remaining'] = remaining
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            id = self.kwargs.get('pk')
            form.save()
            return redirect('payview', pk=id)
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            messages.success(request, 'Enter A Valid Amount.', 'alert-danger')
            return render(request, self.template_name, context)


class StdPayment(LoginRequiredMixin, TemplateView):
    model = Admission
    template_name = "payments/paymentform.html"
    form_class = StudentPayForm

    def get(self, request, *args, **kwargs):
        if 'search' in request.GET:
            form = self.form_class
            search_term = request.GET['search']
            name = Admission.objects.filter(enquiry_id__student_name=search_term).values('enquiry_id__student_name',
                                                                                         'admission_no', 'enquiry_id')
            if not name:
                messages.success(request, 'No Student Found.', 'alert-danger')
                context = {'form': form, 'name': name, 'search-term': search_term}
                return render(request, self.template_name, context)
            else:
                context = {'form': form, 'name': name, 'search-term': search_term}
                return render(request, self.template_name, context)
        else:
            form = self.form_class
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            id = form.cleaned_data['admission_no']
            try:
                qs = Admission.objects.get(admission_no=id)
                enq = qs.enquiry_id
                return redirect('payment', pk=enq)
            except Admission.DoesNotExist:
                form = self.form_class(request.POST)
                messages.success(request, 'Incorrect Admission Number', 'alert-danger')
                context = {}
                context['form'] = form
                return render(request, self.template_name, context)
        else:
            form = self.form_class(request.POST)
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)


class PaymentView(LoginRequiredMixin, TemplateView):
    model = Payment
    template_name = "payments/paymentview.html"

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')

        qs = Payment.objects.filter(enquiry_id=id)
        from django.db.models import Sum
        qs1 = Payment.objects.filter(enquiry_id=id).values('amount', 'enquiry_id').aggregate(total=Sum('amount'))
        qs2 = Admission.objects.get(enquiry_id=id)
        qs3 = Enquiry.objects.get(enquiry_id=id)
        name = qs3.student_name
        fees = qs2.course_fee
        note = qs2.notes
        if (qs1['total'] == None):
            remaining = fees
            msg = "Initial Payment Not Payed"
        else:
            remaining = fees - qs1['total']
            msg = ""
            if remaining == 0:
                msg = "Fees fully paid"
            else:
                pass

        context = {}
        context['name'] = name
        context['payinfo'] = qs
        context['rem_fees'] = remaining
        context['msg'] = msg
        context['info'] = qs2
        context['note'] = note
        return render(request, self.template_name, context)


class PaymentInfo(LoginRequiredMixin, TemplateView):
    model = Admission
    template_name = "payments/paymentinfo.html"
    form_class = StudentPayForm

    def get(self, request, *args, **kwargs):
        if 'search' in request.GET:
            form = self.form_class
            search_term = request.GET['search']

            name = Admission.objects.filter(enquiry_id__student_name=search_term).values('enquiry_id__student_name',
                                                                                         'admission_no', 'enquiry_id')
            if not name:
                messages.success(request, 'No Student Found.', 'alert-danger')
                context = {'form': form, 'name': name, 'search-term': search_term}
                return render(request, self.template_name, context)
            else:
                context = {'form': form, 'name': name, 'search-term': search_term}
                return render(request, self.template_name, context)
        else:
            form = self.form_class
            context = {}
            context['form'] = form
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            id = form.cleaned_data['admission_no']
            try:
                qs = Admission.objects.get(admission_no=id)
                enq = qs.enquiry_id
                return redirect('payview', pk=enq)
            except Admission.DoesNotExist:
                form = self.form_class(request.POST)
                messages.success(request, 'Incorrect Admission Number', 'alert-danger')
                context = {'form': form}
                return render(request, self.template_name, context)
        else:
            form = self.form_class(request.POST)
            context = {'form': form}
            return render(request, self.template_name, context)


@login_required
def signup(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New User Successfully Created', 'alert-success')
            return redirect('index')
        else:
            messages.success(request, 'Invalid Data', 'alert-danger')
    else:
        form = UserRegForm()
    return render(request, 'user_reg.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Successfully Updated', 'alert-success')
            return redirect('index')
        else:
            messages.success(request, 'Invalid Data', 'alert-danger')
    else:
        form = UserRegForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

