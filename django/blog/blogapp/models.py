from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	content = models.CharField(max_length=200)
	written_date = models.DateTimeField('date written')
	def __str__(self):
		return self.content
	def serialize(self):
		data = {
			'content':self.content,
			'written_date':self.written_date
		}
		return data

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	nickname = models.CharField(max_length=128)
	comment = models.TextField()
	country = models.CharField(max_length=128, blank=True)
	phone = models.CharField(max_length=20)
	major = models.CharField(max_length=40)
	instrument = models.CharField(max_length=20)

	def __str__(self):
		return self.nickname

	def serialize(self):
		data = {
			'user':self.user_id,
			'username':self.user.username,
			'email':self.user.email,
			'nickname':self.nickname,
			'comment':self.comment,
			'phone':self.phone,
			'major':self.major,
			'instrument':self.instrument,
		}
		return data

class Music(models.Model):
	name = models.CharField(max_length=40)
	vocal = models.CharField(max_length=40)
	file_name = models.FileField(upload_to='mp3')

	def __str__(self):
		return self.name

	def serialize(self):
		data = {
			'name':self.name,
			'vocal':self.vocal,
			'file_name':self.file_name
		}
		return data

class Picture(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=40)
	comment = models.TextField()
	category = models.CharField(max_length=20)
	picture = models.FileField(upload_to='picture')
	created = models.DateTimeField(auto_now_add=True)

	def serialize(self):
		data = {
			'id':self.id,
			'user':self.user_id,
			'title':self.title,
			'comment':self.comment,
			'category':self.category,
			'picture':self.picture,
			'created':self.created.ctime(),
			'liked':self.like_set.count()
		}
		return data
	def __str__(self):
		return self.title


class Message(models.Model):
	user = models.ForeignKey(User)
	message = models.CharField(max_length=128)
	created = models.DateTimeField(auto_now_add=True)

	def serialize(self):
		data = {
			'id':self.id,
            'user':self.user_id,
            'username':self.user.username,
            'liked':self.like_set.count(),
            'message':self.message,
            'created':self.created.ctime()
		}
		return data


class Like(models.Model):
	user = models.ForeignKey(User)
	message = models.ForeignKey('Message', blank=True)
	picture = models.ForeignKey('Picture', blank=True)
