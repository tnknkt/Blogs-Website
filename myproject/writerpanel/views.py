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
    total = Blogs.objects.filter(writer=writer).aggregate(
        Sum('views'))  # หาผลรวมยอดวิวบทความของนักเขียน 1 คน
    return render(request, "backend/index.html", {"blogs": blogs, 'writer': writer, 'blogCount': blogCount, 'total': total})

@login_required(login_url="member")
def displayForm(request):
    writer = auth.get_user(request)
    categories = Category.objects.all()
    return render(request, "backend/blogForm.html", {"categories": categories, 'writer': writer})

@login_required(login_url="member")
def insertData(request):
    try:
        if request.method == "POST" and request.FILES["image"]:
            datafile = request.FILES["image"]
            # รับค่าจากฟอร์ม
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            writer = auth.get_user(request)

            if str(datafile.content_type).startswith("image"):
                # อัปโหลด
                fs = FileSystemStorage()
                img_url = "blogsImages/"+datafile.name
                filename = fs.save(img_url, datafile)
                # บันทึกข้อมูลบทความ
                blog = Blogs(name=name, category_id=category, description=description,content=content, writer=writer, image=img_url)
                blog.save()

                messages.info(request, ("บันทึกข้อมูลเรียบร้อย"))
                return redirect("displayForm")
            else:
                messages.info(request, ("ไฟล์ที่อัปโหลดไม่รองรับ กรุณาอัปโหลดไฟล์รูปภาพอีกครั้ง"))
                return redirect("displayForm")
    except:
        messages.info(request, ("ไม่สามารถเพิ่มข้อมูลได้ โปรดตรวจสอบข้อมูลอีกครั้ง"))
        return redirect("displayForm")

@login_required(login_url="member")
def deleteData(request, id):
    try:
        blog = Blogs.objects.get(id=id)
        fs = FileSystemStorage()
        # ลบภาพปกของบทความ
        fs.delete(str(blog.image))
        # ลบข้อมูลจากฐานข้อมูลอย่างเดียว
        blog.delete()
        return redirect('panel')
    except:
        return redirect('panel')

@login_required(login_url="member")
def editData(request, id):
    writer = auth.get_user(request)
    blogEdit = Blogs.objects.get(id=id)
    categories = Category.objects.all()
    return render(request, "backend/editForm.html", {"blogEdit": blogEdit, 'categories': categories, 'writer': writer})

@login_required(login_url="member")
def updateData(request, id):
    try:
        if request.method == "POST":
            # ดึงข้อมูลบทความที่ต้องการแก้ไขมาใช้งาน
            blog = Blogs.objects.get(id=id)
            # รับค่าจากฟอร์ม
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]

            # อัปเดตข้อมูล
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()
            messages.info(request, "อัปเดตข้อมูลเรียบร้อย")

        # อัปเดตภาพปก
        if request.FILES["image"]:
            datafile = request.FILES["image"]
            if str(datafile.content_type).startswith("image"):
                # ลบภาพจริงของบทความก่อน
                fs = FileSystemStorage()
                fs.delete(str(blog.image))

                # แทนที่ภาพใหม่
                img_url = "blogsImages/"+datafile.name
                filename = fs.save(img_url, datafile)
                blog.image = img_url
                blog.save()
                return redirect('panel')
    except:
        return redirect('panel')
