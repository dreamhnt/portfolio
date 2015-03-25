from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=20, unique=True)
    comment = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='profileImage/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname

    #제공되는 serializers 모듈은 쓸모없는 데이터도 많이 들어가고 마음대로 수정할수 없어서 직접 커스텀
    def serialize(self):
        if bool(self.picture) == False:     #FileField 예외처리
            picture = None
        else:
            picture = self.picture.url

        data = {
            'user':self.user_id,
            'username':self.user.username,
            'nickname':self.nickname,
            'email':self.user.email,
            'comment':self.comment,
            'picture':self.picture,
            'created':self.created.ctime()
        }
        return data

class Board(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)
    period = models.CharField(max_length=20)
    place = models.CharField(max_length=20)
    capacity = models.CharField(max_length=10)
    picture = models.ImageField(upload_to='boardImage/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


    def serialize(self):
        if bool(self.picture) == False:
            picture = None
        else:
            picture = self.picture.url

        data = {
            'id':self.id,
            'user':self.user_id,
            'nickname':self.user.userprofile.nickname,
            'title':self.title,
            'content':self.content,
            'category':self.category,
            'period':self.period,
            'place':self.place,
            'capacity':self.capacity,
            'picture':picture,
            'created':self.created.ctime()
        }
        return data

class BoardComment(models.Model):
    user = models.ForeignKey(User)
    board = models.ForeignKey('Board')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    def serialize(self):
        data = {
            'id':self.id,
            'user':self.user_id,
            'board':self.board_id,
            'message':self.message,
            'created':self.created.ctime()
        }
        return data
