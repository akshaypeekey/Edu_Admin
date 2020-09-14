from datetime import date

from django.shortcuts import render

from enquiry.models import Enquiry


def base(request):

    enq_today = Enquiry.objects.filter(followup_date=date.today(), status='1')
    count = enq_today.count()
    return {
        'count': count,
        'enq_today': enq_today,
        'user': request.user
    }

