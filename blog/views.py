from django.template import loader
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
    article_data = Article.objects.filter(status='published').order_by('-id')
    list =[]
    for article_data_tag in article_data:
        for tag in article_data_tag.tags.all():
            # print(tag,"oooooooooooooo")
            # x=tag
            list.append(tag)
    count_tag=Counter(list)
    popular_tag = nlargest(3,count_tag,key=count_tag.get)
    # print(c,"wwwwwwwwwwwww")
    # print(new,"qqqqqqqqq")

    con = {"article_data":article_data,"popular_tag":popular_tag}
    return render(request,"main_page.html",con)


def index(request):
    article_data = Article.objects.filter(status='published').order_by('-id')
    list =[]
    for tag in article_data:
        for tag in tag.tags.all():
            list.append(tag)
    count_tag=Counter(list)
    popular_tag = nlargest(3,count_tag,key=count_tag.get)
    con = {"article_data":article_data,"popular_tag":popular_tag}
    return render(request,"index.html",con)


def loginview(request):
    login_form = Userlogin()
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
    con = {"login_form":login_form}
    return render(request,"login.html",con)


def registration(request):
    registration_form = Registration()
    if request.method == "POST":
        registration_form = Registration(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect("loginview")
    else:
        registration_form = Registration()

    con = {"registration_form":registration_form}
    return render(request,"registration.html",con)


def logoutview(request):
    logout(request)
    messages.success(request,'Logout successfully !!!!!!!!!!!!')
    return redirect("loginview")


def article(request):
    # tag=request.POST.get('tag')
    # print(tag)
    if request.method=="POST":
        articleview_form= articleview(request.POST,request.FILES)
        tags=request.POST["tags"]
        split_tag=tags.split(',')
        # print(obj)
        # obj.save()
            # print(tags)
        if articleview_form.is_valid():
            articleview_form.instance.user = request.user
            article = articleview_form.save()
            for tag in split_tag:
                tags = Tag.objects.filter(tag__iexact=tag).first()
                if not tags:
                    tags=Tag.objects.create(tag=tag)
                article.tags.add(tags.id)
            return redirect("main_page")
    else:
        articleview_form=articleview()
    con = {"articleview_form":articleview_form}
    return render(request,"article.html",con)


def draft(request):
    article_data = Article.objects.filter(status='draft',user=request.user).order_by('-id')
    con = {"article_data":article_data}
    return render(request,"draft.html",con)

def edit_draft(request,id):
    article_data_id=Article.objects.get(id=id)
    dgdg=list(article_data_id.tags.values_list("tag",flat=True))
    exists= [str(x).strip() for x in dgdg]
    if request.method=="POST":
        articleview_form=articleview(request.POST,request.FILES,instance=article_data_id)
        get_tags=request.POST["tags"]
        split_tag=get_tags.split(',')
        split_tag= [str(x).strip() for x in split_tag]
        if articleview_form.is_valid():
            article = articleview_form.save()
            for tags in exists:
                if str(tags).strip() not in split_tag:
                    tag = Tag.objects.filter(tag__iexact=tags.strip()).first()
                    article.tags.remove(tag.id)
            for tag in split_tag:
                if str(tag).strip() not in exists:
                    tags = Tag.objects.filter(tag__iexact=tag.strip()).first()
                    if not tags:
                        tags=Tag.objects.create(tag=tag)
                    article.tags.add(tags.id)
            return redirect("main_page")
    else:
        articleview_form=articleview(instance=article_data_id)
        # print(articleview_form,"1111111111111111")
    con = {"articleview_form":articleview_form,"x":str(exists).replace("]","").replace("[","").replace("'","")}
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