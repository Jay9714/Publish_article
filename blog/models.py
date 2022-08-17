# from tkinter import CASCADE
# from turtle import title
from django.db import models
from django.contrib.auth.models import User
# from taggit.managers import TaggableManager


# Create your models here.


class Tag(models.Model):
    tag = models.CharField(max_length=500)

    def __str__(self):
        return self.tag
        
class Article(models.Model):
    STATUS_CHOICES=(
        ('draft','draft'),
        ('published','published'),
    )

    user= models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    content=models.CharField(max_length=500)
    img=models.ImageField(upload_to='img')
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags = models.ManyToManyField(to=Tag, blank=True)
  
    # def __str__(self):
    #     return self.title




# class Article_tag(models.Model):
#     article = models.ForeignKey(Article,on_delete=models.CASCADE)
#     tag = models.ForeignKey(Tag,on_delete=models.CASCADE)