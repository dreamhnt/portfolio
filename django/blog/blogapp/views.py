from django.shortcuts import render
from blogapp.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
# Create your views here.
#login decorator
from django.contrib.auth import authenticate, login, logout
import base64
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from blogapp.models import *
from django.core import serializers #json serialize module
from django.core.files import File
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile
from django.contrib import messages


@login_required
def main_page(request):
	return render_to_response(
		'main_page.html',
		RequestContext(request,	{
			'user': request.user,
		 }))

def login_page(request):
	return render_to_response(
		'registration/login.html',
		RequestContext(request)
		)
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')


def profile(request):
	return render_to_response(
		'profile.html',
		RequestContext(request)
		)
@login_required
def notice_page(request):
	return render_to_response(
		'notice_page.html',
		RequestContext(request)
		)
@login_required
def gallery_page(request):
	all_pictures = Picture.objects.all().order_by('-written_date')
	variables = RequestContext(request,{
		'all_articles': all_pictures,
		})
	return render_to_response('gallery_page.html', variables)

def picture_up(request):
	if request.method == 'POST':
    #Picture 모델 불러옴
		picture = Picture()
		title = request.POST['title']
    #file 불러옴
		f = request.FILES['imgfile']
		picture.user = request.user
		picture.title = title
		picture.comment = request.POST['writearea']
		picture.category = request.POST['category']
     #request.FILES 로 불러온 파일을 업로드한 이름 그대로 문자열로 변환
		file_name = "%s" % f
    #파일 저장하기 위한 메소드
		picture.picture.save(file_name ,f)
		picture.save()
		return HttpResponseRedirect('/gallery_page')
	else:
		return HttpResponse('request error')

def gallery(request):
	# result = Pucture.objects.order_by('-created').all()
	result = Picture.objects.order_by('-created').all()
	return toJSON(result)
	#serialized_obj = serializers.serialize('json', result, ensure_ascii=False)
	#return HttpResponse(serialized_obj, content_type='application/json; charset=utf-8')
def like_view(request):
	try:
		query = request.GET.get('query','')
		picture = Picture.objects.get(id=query)
		like = Like()
		like.user = request.user
		like.picture = picture
		like.save()
	except:
		return toJSON({'status':'bad request'},400)
	return toJSON({'status':'created'})

def music_page(request):
	return render_to_response(
		'music_page.html',
		RequestContext(request)
		)

def search_page(request):

	query = request.GET.get('query','')

	result = Music.objects.filter(name__contains=query)

	serialized_obj = serializers.serialize('json', result, ensure_ascii=False)

	return HttpResponse(serialized_obj, content_type='application/json; charset=utf-8')

def musicbox(request):

	query = request.GET.get('query','')

	result = Music.objects.filter(id=query)

	serialized_obj = serializers.serialize('json', result, ensure_ascii=False)

	return HttpResponse(serialized_obj, content_type='application/json; charset=utf-8')




#@csrf_protect
def login_check(request):
	if request.method == 'POST':
		if not request.POST.get('remember_me', None):  # 로그인이 체크 되지 않았을때 브라우저 닫으면 세션이 제거된다.
			 request.session.set_expiry(0)  # 세선 제거 메서드 0 value로 시간 설정 가능.

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				HttpResponseRedirect('/')
			else:
				HttpResponseRedirect('/')
		else:
			HttpResponseRedirect('/')
	return HttpResponseRedirect('/')

def register_page(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		if User.objects.filter(username__exact=username).count():
			return HttpResponse('duplicate id',400)
		user = User.objects.create_user(username,password=password,email=email)
		user.save()
		profile = UserProfile()
		profile.user = user
		profile.save()
		return HttpResponseRedirect('/')
	else:
		return HttpResponse('bad request')

class MyJSONEncoder(DjangoJSONEncoder):				# FileFields 를 json에맞게 Encoder
    def default(self, obj):
        if isinstance(obj, FieldFile):
            return obj.url
        return super(MyJSONEncoder, self).default(obj)

def toJSON(objs, status=200):			#model 객체를 JSON serialize
	j = json.dumps(
        [picture.serialize() for picture in objs],
        cls = MyJSONEncoder,
        ensure_ascii = False)
	return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')


# one line blog
def Oneblog(request):
	all_articles = Message.objects.all().order_by('-created')
	variables = RequestContext(request,{
		'all_articles': all_articles,
		'message': 'Write something!'
		})
	return render_to_response('one_page.html', variables)


def submit(request):
	try:
		cont = request.POST['content']
	except(KeyError):
		variables = RequestContext(request,{
		'all_articles': all_articles,
		'message': 'Failed to read content'
		})
		return render_to_response('one_page.html', variables)


	else:
		article = Message(message=cont, created=timezone.now())
		article.user = request.user
		article.save()
		return HttpResponseRedirect('/one_page')

def remove(request, article_id):
	try:
		article = Message.objects.get(id=article_id)
		if article.user == request.user:
			article.delete()
			return HttpResponseRedirect('/one_page')
		else:
			return HttpResponse('deny permission')
	except:
		return HttpResponse('not found')
