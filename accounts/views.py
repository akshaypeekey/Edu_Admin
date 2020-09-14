# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
#
# # Create your views here.
# from django.views.generic import TemplateView
#
# from enquiry.forms import UserRegForm
#
#
# class UserReg(TemplateView):
#     model=User
#     template_name = "user_reg.html"
#     form_class=UserRegForm
#
#     def get(self, request, *args, **kwargs):
#         context={}
#         context['userform']=self.form_class
#         return render(request,self.template_name,context)
#
#     def post(self, request, *args, **kwargs):
#         form=self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         else:
#             form = self.form_class(request.POST)
#             context = {}
#             context['userform'] = form
#             return render(request, self.template_name, context)
#
# class UserLogin(TemplateView):
#     model=User
#     template_name = "login.html"
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)
#
#     def post(self, request, *args, **kwargs):
#         uname=request.POST.get('username')
#         pwd=request.POST.get('password')
#         user=authenticate(request,username=uname,password=pwd)
#         if user is not None:
#             login(request,user)
#
#         else:
#             context={}
#             message="Incorrect username or password"
#             context['message']=message
#             return render(request, self.template_name,context)
#
# def userlogout(request):
#     logout(request)
#     return redirect('login')
#
#
