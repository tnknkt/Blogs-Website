from fileinput import filename
from django.shortcuts import redirect, render
from blogs.models import Blogs
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.
@login_required(login_url="member")
def panel(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    total = Blogs.objects.filter(writer=writer).aggregate(Sum('views')) # หาผลรวมยอดวิวบทความของนักเขียน 1 คน
    return render(request,"backend/index.html",{"blogs":blogs,'writer':writer,'blogCount':blogCount,'total':total})

def displayForm(request):
    categories = Category.objects.all()
    return render(request,"backend/blogForm.html",{"categories":categories,})

def insertData(request):
    if request.method == "POST" and request.FILES["image"]:
        datafile = request.FILES["image"]
        if str(datafile.content_type).startswith("image"):
            # อัปโหลด
            fs = FileSystemStorage()
            img_url = "blogsImages/"+datafile.name
            filename = fs.save(img_url,datafile)
            messages.info(request,("อัปโหลดไฟล์รูปภาพเรียบร้อย"))
            return redirect("displayForm")
        else:
            messages.info(request,("ไฟล์ที่อัปโหลดไม่รองรับ กรุณาอัปโหลดไฟล์รูปภาพอีกครั้ง"))
            return redirect("displayForm")