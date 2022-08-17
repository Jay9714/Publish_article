from genericpath import exists
from multiprocessing.sharedctypes import Value
from optparse import Values
from django.contrib import messages
from django.shortcuts import render,redirect

from .models import Article,Tag
from .forms import Userlogin,Registration,articleview
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from collections import Counter
from heapq import nlargest

def main_page(request):
    # tag=Article.tags.most_common()[0:2]
    # print(tag)
    list =[]
    data = Article.objects.filter(status='published')
    for tag in data:
        for tag in tag.tags.all():
            # print(tag,"oooooooooooooo")
            # x=tag
            list.append(tag)
    c=Counter(list)
    popular_tag = nlargest(3,c,key=c.get)
    # print(c,"wwwwwwwwwwwww")
    # print(new,"qqqqqqqqq")

    article_data = Article.objects.filter(status='published').order_by('-id')
    con = {"article_data":article_data,"data":data,"popular_tag":popular_tag}
    return render(request,"main_page.html",con)


def index(request):
    list =[]
    data = Article.objects.filter(status='published')
    for tag in data:
        for tag in tag.tags.all():
            list.append(tag)
    c=Counter(list)
    popular_tag = nlargest(3,c,key=c.get)
    article_data = Article.objects.filter(status='published').order_by('-id')
    con = {"article_data":article_data,"popular_tag":popular_tag,"data":data}
    return render(request,"index.html",con)


def loginview(request):
    form = Userlogin()
    if request.method == 'POST':
        uname = request.POST['username']
        upass = request.POST['password']
        user = authenticate(username=uname,password=upass)
        if user is None:
            messages.warning(request,'Please Enter Correct Credinatial')
            return redirect('/loginview/')
        else:
            login(request,user)
        return redirect('main_page')
    else:
        pass
        # if request.user.is_authenticated:
        #     return redirect('main_page')
        # else:
        #     pass
    con = {"form":form}
    return render(request,"login.html",con)


def registration(request):
    form = Registration()
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect("loginview")
    else:
        form = Registration()

    con = {"form":form}
    return render(request,"registration.html",con)


def logoutview(request):
    logout(request)
    messages.success(request,'Logout successfully !!!!!!!!!!!!')
    return redirect("loginview")


def article(request):
    # tag=request.POST.get('tag')
    # print(tag)
    if request.method=="POST":
        form= articleview(request.POST,request.FILES)
        tags=request.POST["tags"]
        obj=tags.split(',')
        # print(obj)
        # obj.save()
            # print(tags)
        if form.is_valid():
            form.instance.user = request.user
            ob = form.save()
            for x in obj:
                tags = Tag.objects.filter(tag__iexact=x).first()
                if not tags:
                    tags=Tag.objects.create(tag=x)
                ob.tags.add(tags.id)
            return redirect("main_page")
    else:
        form=articleview()
    con = {"form":form}
    return render(request,"article.html",con)


def draft(request):
    article_data = Article.objects.filter(status='draft',user=request.user).order_by('-id')
    con = {"article_data":article_data}
    return render(request,"draft.html",con)

# object.tags.clear()
# for tag in data['tags']:
#     object.tags.add(tag)
def edit_draft(request,id):
    article_data_id=Article.objects.get(id=id)
    # article_tag=Tag.objects.get(id=id)
    data = Article.objects.filter()
    if request.method=="POST":
        form=articleview(request.POST,request.FILES,instance=article_data_id)
        tags=request.POST["tags"]
        obj=tags.split(',')
        if form.is_valid():
            form.instance.user = request.user
            ob = form.save()
            for x in obj:
                tags = Tag.objects.filter(tag__iexact=x).first()
                if not tags:
                    tags=Tag.objects.create(tag=x)
                ob.tags.add(tags.id)
            return redirect("main_page")
    else:
        form=articleview(instance=article_data_id)
    con = {"form":form}
    return render(request,"article.html",con)


def delete_draft(request,id):
    article_data_id=Article.objects.get(id=id)
    article_data_id.delete()
    return redirect("draft")


def delete_article(request,id):
    article_data_id = Article.objects.get(id=id)
    article_data_id.delete()
    return redirect("main_page")

def tag_post(request,id):
    tag_data = Article.objects.filter(tags=id,status="published")
    con = {"tag_data":tag_data}
    return render(request,"tagpost.html",con)

def tag_delete(request,id,tag_id):
    tag_data = Article.objects.get(id=id)
    tag_data.tags.remove(tag_id)
    return redirect("draft")