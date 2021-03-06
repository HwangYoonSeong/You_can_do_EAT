from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Food, Ingredient, Post, Comment, User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
from django.conf import settings
import json, os
import sys
import urllib.request

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, "test.html")

@csrf_exempt
def post_user(request):
    if request.method == "POST":
        user = User()
        data = json.loads(request.body.decode('utf-8'))
        user.uid = data["uid"]
        user.userImg = data["userImg"]
        user.email = data["email"]
    
        try: # 로그인 체크
            query = User.objects.all().get(uid=user.uid)

        except: # 신규 로그인
            user.save()

    return render(request, "test.html")

@csrf_exempt
def post_post(request):
    if request.method == "POST":
        post = Post()
        post.title = request.POST["title"]
        post.contents = request.POST["content"]
        post.writerID = request.POST["uid"]
        query = list(User.objects.filter(uid=request.POST["uid"]).values())[0]
        post.writer = query["email"]
        post.userImg = query["userImg"]
        post.save()

        try:
            postImg = request.FILES["postImg"]
            postImg.name = str(post.id) + '.png'
            Post.objects.filter(id=post.id).update(postImg='static/post/' + str(post.id) + '.png')
            default_storage.save(str(settings.BASE_DIR) + '/ycde/static/post/' + postImg.name, postImg)

        except:
            return render(request, "test.html")

    return render(request, "test.html")
        
@csrf_exempt
def post_comment(request):
    if request.method == "POST":
        comm = Comment()
        data = json.loads(request.body.decode('utf-8'))
        comm.pid = data["pid"]
        comm.contents = data["contents"]
        query = list(User.objects.filter(uid=data["uid"]).values())[0]
        comm.writer = query["email"]
        comm.writerImg = query["userImg"]
        comm.save()

    return render(request, "test.html")
        
@csrf_exempt
def get_postlist(request):
    if request.method == "GET":
        post = Post.objects.all()
        reslist = []
        for idx, p in enumerate(post):
            res = {}
            res['pid'] = str(p.id)
            res['title'] = str(p.title)
            res['content'] = str(p.contents)
            date = str(p.date).split(':')[:-1]
            date.insert(-1, ':')
            res['date'] = ''.join(date)
            res['writer'] = str(p.writer)
            res['postImg'] = str(p.postImg)
            reslist.append(res)

        page = int(request.GET['page'])
        reslist.reverse()
        startidx = page * 20
        endidx = (page + 1) * 20

        return JsonResponse({'results':reslist[startidx:endidx]})

@csrf_exempt
def get_post(request):
    if request.method == "GET":
        res = {}
        post = list(Post.objects.filter(id=request.GET["pid"]).values())[0]
        res['writer'] = str(post['writer'])
        date = str(post['date']).split(':')[:-1]
        date.insert(-1, ':')
        res['date'] = ''.join(date)
        res['title'] = str(post['title'])
        res['content'] = str(post['contents'])
        res['postImg'] = str(post['postImg'])
        user = list(User.objects.filter(uid=post['writerID']).values())[0]
        res['userImg'] = str(user['userImg'])
        res['comments'] = []

        comments = Comment.objects.filter(pid=request.GET["pid"])
        for idx, c in enumerate(comments):
            comm = {}
            comm['id'] = str(c.id)
            comm['writerImg'] = str(c.writerImg)
            comm['writer'] = str(c.writer)
            comm['contents'] = str(c.contents)
            cdate = str(c.date).split(':')[:-1]
            cdate.insert(-1, ':')
            comm['date'] = ''.join(cdate)
            res['comments'].append(comm)

    return JsonResponse({'results':res})

def encode_bit(bit):
    cnt = Ingredient.objects.count()
    ingredientList = []

    for i in range(cnt):
        ingredientDict = {}
        fbit = bit & (2**i)
        ing = list(Ingredient.objects.values())[i]
        ingredientDict['name'] = ing['name']
        ingredientDict['image'] = ing['image']
        if fbit == 0:
            ingredientDict['checked'] = False
        else:
            ingredientDict['checked'] = True
        ingredientList.append(ingredientDict)
    
    return ingredientList

@csrf_exempt
def get_ingredientlist(request):
    if request.method == "GET":
        post = list(User.objects.filter(uid=request.GET["uid"]).values())[0]
        ingredientList = encode_bit(post['filterBit'])

        return JsonResponse({"results":ingredientList})


@csrf_exempt
def post_filterBit(request):
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(uid=data['uid']).update(filterBit=data['filterBit'])

    return render(request, "test.html")

@csrf_exempt
def get_postSearch(request):
    if request.method == "GET":
        post = list(Post.objects.filter(title__icontains=request.GET["input"]).values())
        reslist = []

        for idx, p in enumerate(post):
            res = {}
            res['pid'] = str(p['id'])
            res['title'] = str(p['title'])
            res['content'] = str(p['contents'])
            date = str(p['date']).split(':')[:-1]
            date.insert(-1, ':')
            res['date'] = ''.join(date)
            res['writer'] = str(p['writer'])
            res['postImg'] = str(p['postImg'])
            reslist.append(res)

        return JsonResponse({'results':reslist})

alergy = {
    "메밀":["메밀"],
    "밀":["밀"],
    "대두":["대두"],
    "호두":["호두"],
    "땅콩":["땅콩"],
    "복숭아":["복숭아"],
    "토마토":["토마토"],
    "돼지고기":["돼지"],
    "난류":["난류", "계란", "알", "달걀"],
    "우유":["우유", "버터", "요구르트", "요거트", "치즈"],
    "닭고기":["닭"],
    "쇠고기":["쇠고기", "소고기"],
    "새우":["새우"],
    "고등어":["고등어"],
    "홍합":["홍합"],
    "전복":["전복"],
    "굴":["굴"],
    "조개류":["조개"],
    "게":["게"],
    "오징어":["오징어"],
    "아황산":["아황산"],
}

@csrf_exempt
def get_foodSearch(request):
    if request.method == "GET":
        res = []
        try:
            user = list(User.objects.filter(uid=request.GET["uid"]).values())[0]
            food = list(Food.objects.filter(name=request.GET["result"]).values())[0]
            idlist = food['ingredientDetail'].split(',')

            bit = food['ingredientBit'] & user['filterBit']
            
        except:
            if request.GET["uid"]=='':
                food = list(Food.objects.filter(name=request.GET["result"]).values())[0]
                idlist = food['ingredientDetail'].split(',')
                bit = food['ingredientBit'] & 0

            else: # food not exist
                return JsonResponse({'results' : res[:-1]})

        for indetail in idlist: 
            resdict = {}
            resdict['ingredient'] = indetail
            resdict['danger'] = False
            for idx, a in enumerate(alergy):
                match = bit & (2**idx)
                if match == 0:
                    continue
                else:
                    for ingred in alergy[a]:
                        if ingred in indetail:
                            resdict['danger'] = True
                            break
            res.append(resdict)
        
        print(res[:-1])

        return JsonResponse({'results' : res[:-1]})

def get_translate(request):
    client_id = "omCYkh439Kfoa56Tpjjm" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "TIXxlALgvd" # 개발자센터에서 발급받은 Client Secret 값
    encText = request.GET['text']
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        res = response_body.decode('utf-8')
        res = json.loads(res)
        return JsonResponse(res)

    else:
        return JsonResponse({})
    
    
def get_translateFood(request):
    client_id = "omCYkh439Kfood6Tpjjm" # 개발자센터에서 발급받은 Client ID 값
    client_secret = "TIXxlALgvd" # 개발자센터에서 발급받은 Client Secret 값
    encText = request.GET['text']
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        res = response_body.decode('utf-8')
        res = json.loads(res)
        return JsonResponse(res)

    else:
        return JsonResponse({})