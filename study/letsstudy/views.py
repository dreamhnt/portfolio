from django.shortcuts import render, render_to_response
from letsstudy.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import json
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q      #복잡한 queryset 사용하기위해 (검색에 or 수행)
from endless_pagination.decorators import page_template
# Create your views here.


def serialize(objs):
    serialized=[]
    for obj in objs:
        serialized.append(obj.serialize())
    return serialized

def toJSON(objs, status=200):
    j = json.dumps(objs, ensure_ascii=False)
    return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')

'''
def main_page(request):
    return render_to_response(
        'index.html',
        RequestContext(request, {
            'user': request.user,
        })
    )
'''
def main_page(request, template='index.html', page_template='bbs_list.html'):
    if bool(request.GET):
        q = request.GET['search']
        bbs = Board.objects.filter(Q(content__contains=q) | Q(title__contains=q)).order_by('created')
    else:
        bbs = Board.objects.order_by('-created').all()
    context = {
        'user': request.user,
        'bbs': bbs,
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))

def detail_page(request, num):
    num = int(num[:-1])         # num 값이 '232/' 이런 문자열로 넘어오기때문에 마지막 '/'를 제거해주고 변환한다.
    bbs = Board.objects.get(id=num)
    comments = BoardComment.objects.filter(board=bbs)
    print(bbs.user.userprofile.picture)
    return render_to_response(
        'detail.html',
        RequestContext(request, {
            'user': request.user,
            'datas': bbs,
            'comments': comments,
        })
    )


'''
@csrf_exempt
def bbs(request, method):
    if method == 'search':
        q = request.GET['query']
        bbs = Board.objects.filter(Q(content__contains=q) | Q(title__contains=q)).order_by('created')
        return toJSON(serialize(bbs))
    elif method == 'list':
        bbs = Board.objects.order_by('-created').all()
        return toJSON(serialize(bbs))
'''
@csrf_exempt
def comment(request):
    if request.method == 'POST':
        comment = BoardComment()
        bbs_id = request.POST['bbs_id']
        comment.message = request.POST['comment']
        comment.user = request.user
        bbs = Board.objects.get(id=bbs_id)  #댓글에 게시글 번호 연결
        comment.board = bbs
        comment.save()

        return HttpResponseRedirect('/detail/' + bbs_id)
    else:
        return toJSON({'status':'bad request'},400)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            nickname = request.POST['nickname']
            phone = request.POST['phone']
            if User.objects.filter(username__exact=username).count():
                return toJSON({'status':'idFail'},400)
            if UserProfile.objects.filter(nickname__exact=nickname).count():
                return toJSON({'status':'nicknameFail'},400)
            user = User.objects.create_user(username, password=password, email=email)
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.nickname = nickname
            profile.phone = phone
            profile.save()
            return toJSON({'status':'success'})
        except:
            return toJSON({'status':'create fail'}, 400)
    else:
        return toJSON({'status':'bad request'},400)



def login_page(request):
    return render_to_response('registration/login.html')

def dologout(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def login_check(request):
    if request.method == 'POST':
        #로그인유지 체크가 안되 있으면 지우고 되있면 Django 기본값인 2주가 된다.
        if not request.POST.get('remember',None):
            request.session.set_expiry(0)

        username = request.POST['username']
        password = request.POST['password']

        #User가 있으면 객체 반환, 아니면 아무것도 반환 안한다(None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return toJSON({'status':'login success'})    #올바르며 사용가능
            else:
                return toJSON({'status':'not_active User'},400)    #확인되었지만 활성화되지 않은 사용자
        else:
            return toJSON({'status':'login fail'},400)  #아이디나 패스워드가 잘못됨
    else:
        return toJSON({'status':'bad request'},400)

@login_required(login_url='login/')
def write_page(request):
    return render_to_response(
        'write_page.html',
        RequestContext(request, {
            'user': request.user,
        })
    )

@csrf_exempt
def write(request):
    if request.method == 'POST':
        try:
            mydict = request.POST
            board = Board()
            board.user = request.user
            board.title = mydict['title']
            board.content = mydict['content']
            board.category = mydict['category']
            board.capacity = mydict['capacity']
            board.place = mydict['place']
            board.period = mydict['period']
            #파일을 불러온후 문자열로 변환한 이름으로 저장한다.
            if request.method == 'FILES':
                f = request.FILES['picture']
                file_name = "%s" % f
                board.picture.save(file_name, f)

            board.save()
            return HttpResponseRedirect('/')
        except:
            return toJSON({'status':'create fail'}, 400)
    else:
        return toJSON({'status':'bad request'},400)

def test_page(request):
    return render_to_response('test.html')
