"""Enquiry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from enquiry.views import *
urlpatterns = [
    path('createenq',createenq,name='createenq'),
    path('viewenq/<str:pk>',ViewEnquiry.as_view(),name='viewenq'),
    path('listenq', EnquiryList.as_view(), name='listenq'),
    path('updateenq/<str:pk>',updateenq,name='updateenq'),
    path('deleteenq/<str:pk>',DeleteEnquiry.as_view(),name='deleteenq'),
    path('followup',FollowUp.as_view(),name='followup'),
    path('followupdetail/<str:pk>',FollowUpDetail.as_view(),name='followupdetail'),
    path('viewfollowup',ViewFollowUp.as_view(),name='viewfollowup'),
    path('viewinfo/<str:pk>',StudentInfoFollow.as_view(),name='viewinfo'),

    path('counselloradd',CounsellorCreation.as_view(),name='counselloradd'),
    path('deletecounsellor/<str:pk>', DeleteCounsellor.as_view(), name='deletecounsellor'),
    path('counsellorreport/<str:pk>', CounsellorReport.as_view(), name='counsellorreport'),

    path('',Index.as_view(),name='index'),
    path('listadm', AdmitionList.as_view(), name='listadm'),
    path('listadt', AdmittedList.as_view(), name='listadt'),
    path('report/<str:pk>', ReportUpdate.as_view(), name='report'),

    #      course urls
    path('createcourse',CourseCreation.as_view(),name='createcourse'),
    path('viewcourse',ViewCourse.as_view(),name='viewcourse'),
    path('courseupdate/<int:pk>',CourseUpdation.as_view(),name='courseupdate'),
    path('deletecourse/<int:pk>',CourseDelete.as_view(),name='deletecourse'),

#      batch urls
    path('createbatch',BatchCreation.as_view(),name='createbatch'),
    path('viewbatch',BatchView.as_view(),name='viewbatch'),
    path('updatebatch/<int:pk>',BatchUpdate.as_view(),name='updatebatch'),
    path('deletebatch/<int:pk>',BatchDelete.as_view(),name='deletebatch'),

#  admission
    path('paymentform/<str:pk>',NewAdmission.as_view(),name='newadmission'),
    path('payment/<str:pk>',StudentPayment.as_view(),name='payment'),
    path('studentpay',StdPayment.as_view(),name='studentpay'),
    path('payview/<str:pk>',PaymentView.as_view(),name='payview'),
    path('payinfo',PaymentInfo.as_view(),name='payinfo'),

    path('register', signup, name= 'register'),
    path('profile', edit_profile, name= 'profile'),



]
