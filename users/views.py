from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from users.forms import RegisterForm,LoginForm,PasswordChangeForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from users.tasks import send_email_task
from users.models import CustomUser
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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
    

class PasswordResetView(View):
    def get(self,request):
        return render(request,'registration/password_reset.html')
    
    def post(self,request):
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(f"/users/password-reset-confirm/{uid}/{token}/")

            send_email_task.delay(
                subject='Parolni tiklash',
                message=f"Parolingizni tiklash uchun xavola:{reset_link}",
                recipient_list=[user.email]
            )
        return redirect('password_reset_done')

class PasswordResetDoneView(View):
    def get(self,request):
        return render(request,'registration/password_reset_done.html')
    

class PasswordResetConfirmView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        return render(request,'registration/password_reset_confirm.html',context)
    
    def post(self,request,uidb64,token):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            messages.error(request,'Parollar mos kelmadi')
            return redirect(request.path)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError):
            messages.error(request,'Havola yaroqsiz')
            return redirect('password_reset')
        
        if default_token_generator.check_token(user,token):
            user.set_password(password1)
            user.save()
            send_email_task.delay(
                subject="Parol tiklandi",
                message="Parolingiz muvaffaqiyatli tiklandi",
                recipient_list=[user.email]
            )
            return redirect('password_reset_complete')
        else:
            messages.error(request,'Havola yaroqsiz yoki eskirgan')
            return redirect('password_reset')
        

class PasswordResetCompleteView(View):
    def get(self,request):
        return render(request,'registration/password_reset_complete.html')
    
        
    
        


    
    

    
    



    

