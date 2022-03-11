from email import message
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request,"backend/login_register.html")

def register(request):
    if request.method ==  "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if username == "" or email == "" or password == "" or repassword == "":
            messages.info(request,"กรุณาป้อนข้อมูลให้ครบถ้วน")
            return redirect("member")
        else:
            if password == repassword:
                if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists(): # exists() เช็ค Username ซ้ำ
                    messages.info(request,"Username และ Email นี้เคยลงทะเบียนไปแล้ว")
                    return redirect("member")
                elif User.objects.filter(username=username).exists(): # exists() เช็ค Username ซ้ำ
                    messages.info(request,"Username นี้มีคนใช้แล้ว")
                    return redirect("member")
                elif User.objects.filter(email=email).exists(): # exists() เช็ค Username ซ้ำ
                    messages.info(request,"Email นี้เคยลงทะเบียนไปแล้ว")
                    return redirect("member")
                else:
                    user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                    )
                    user.save()
                    messages.info(request,"สร้างบัญชีเรียบร้อย")
                    return redirect("member")
            else:
                messages.info(request,"ไม่สามารถลงทะเบียนได้ รหัสผ่านไม่ตรงกัน")
                return redirect("member")
    