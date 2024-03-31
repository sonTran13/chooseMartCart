from django.shortcuts import render
from .models import MyAccountManager
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Account

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if Account.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if Account.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        user = Account.objects.create_user(first_name=fname, last_name=lname, username=username, email=email, password=pass1)
        # user.is_active = True
        # user.is_email_verified = True
        # user.save()
        messages.success(request, "Your Account has been created succesfully!!")
        return redirect('signin')
    return render(request, "signup.html")

# def signin(request):
#     if request.method == 'POST':
#         context={'data':request.POST}
#         username = request.POST['username']
#         password = request.POST['password']
#         if not Account.objects.filter(username=username).exists():
#             messages.error(request, 'Invalid Username')
#             return redirect('signin')
        
#         user = authenticate(username=username, password=password)
#         if user is None:
#             # Display an error message if authentication fails (invalid password)
#             messages.error(request, "Invalid Password")
#             return redirect('signin')

#         login(request, user)
#         return redirect('home') 
#     return render(request, "signin.html")
def signin(request):
    if request.method == 'POST':
        context = {'data': request.POST}
        username = request.POST['username']
        password = request.POST['password']

        # Kiểm tra xem tài khoản có tồn tại không
        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            messages.error(request, 'Invalid Username')
            return redirect('signin')
        
        # Xác thực người dùng bằng cách sử dụng phương thức authenticate của model Account
        user = user.authenticate(request, username=username, password=password)
        
        if user is None:
            # Hiển thị thông báo lỗi nếu xác thực không thành công (mật khẩu không hợp lệ)
            messages.error(request, "Invalid Password")
            return redirect('signin')

        # Đăng nhập người dùng
        login(request, user)
        return redirect('home') 
    return render(request, "signin.html")


def signout(request):
        logout(request)
        messages.success(request, "Logged Out Successfully!!")
        return redirect('home')