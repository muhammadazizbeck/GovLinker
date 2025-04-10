from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from users.forms import RegisterForm,LoginForm,PasswordChangeForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from users.tasks import send_email_task

# Create your views here.

class RegisterView(View):
    def get(self,request):
        form = RegisterForm()
        context = {
            'form':form
        }
        return render(request,'registration/register.html',context)
    
    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email_task.delay(
                subject = 'Welcome to our Web-site',
                message = "Thank you for registering use",
                recipient_list = [user.email]
            )
            return redirect('login')
        else:
            context = {
                'form':form
            }
            return render(request,'registration/register.html',context)

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                send_email_task.delay(
                    subject="Login Successful",
                    message=f"Hi {user.username}, you have logged in successfully.",
                    recipient_list=[user.email]
                )
                return redirect('home')
            else:
                return render(request, 'registration/login.html', {
                    'form': form,
                    'error': 'Username yoki parol noto‘g‘ri!'
                })

        return render(request, 'registration/login.html', {'form': form})
    
class LogoutView(View):
    def post(self,request):
        logout(request)
        return redirect('login')
    
class PasswordChangeView(View):
    def get(self,request):
        form = PasswordChangeForm(user=request.user)
        context = {
            'form':form
        }
        return render(request,'registration/password_change.html',context)
    
    def post(self,request):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            new_password=form.cleaned_data.get('new_password1')
            user=request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request,user)
            send_email_task.delay(
                subject="Password Changed Successfully",
                message="Your password has been successfully changed.",
                recipient_list=[user.email]
            )
            messages.success(request,"Parolingiz muvaffaqiyatli o'zgartirildi")
            return redirect('password_change_done')
        context = {
            'form':form
        }
        return render(request,'registration/password_change.html',context)
    
class PasswordChangeDoneView(View):
    def get(self,request):
        return render(request,'registration/password_change_done.html')
    
    



    

