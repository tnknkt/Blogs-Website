from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs
from django.core.paginator import Paginator , EmptyPage , InvalidPage

# หน้า Index.
def index(request):
    categories = Category.objects.all()
    blogs = Blogs.objects.all()
    latest = Blogs.objects.all().order_by('-pk')[:2] # ('-pk')=เรียงมากไปน้อย [:2]=แสดงแค่ 2 เนื้อหา 

    #บทความยอดนิยม
    poppular = Blogs.objects.all().order_by('-views')[:3] # เรียงมากไปน้อย 3 ตัวแรก

    #บทความแนะนำ
    suggestion = Blogs.objects.all().order_by('views')[:3] # น้อยไปมาก 3 ตัวแรก


    #Pagination
    paginator = Paginator(blogs,4) # แสดงเนื้อหา 3 เนื้อหา ต่อ 1 หน้า
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        blogPerpage = paginator.page(page)
    except (EmptyPage,InvalidPage): # หาหน้าไม่เจอ,หาเนื้อหาไม่เจอ = เปิดไปหน้าสุดท้าย
        blogPerpage = paginator.page(paginator.num_pages)

    return render(request,"frontend/index.html",{'categories':categories,'blogs':blogPerpage,'latest':latest,'poppular':poppular,'suggestion':suggestion})

# หน้ารายละเอียด.
def blogDetail(request,id):
    categories = Category.objects.all() #หมวดหมู่
    poppular = Blogs.objects.all().order_by('-views')[:3] # บทความยอดนิยม
    suggestion = Blogs.objects.all().order_by('views')[:3] # บทความแนะนำ น้อยไปมาก 3 ตัวแรก
    singleBlog = Blogs.objects.get(id=id)
    singleBlog.views = singleBlog.views+1
    singleBlog.save()
    return render(request,"frontend/blogDetail.html",{"blog":singleBlog,'categories':categories,'poppular':poppular,'suggestion':suggestion})
