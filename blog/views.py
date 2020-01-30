from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from . models import article, CurrentUserSerializer
import json
def register(request):
    if 'register' in request.POST:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'register.html',{'error_message':"Username already taken"})
            else:
                user= User.objects.create_user(username = username, password = password1)
                user.save()
                return redirect('/')
        else:
            return render(request,'register.html',{'error_message':"Password does not match"})
    return render(request,'register.html')
def login(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            return redirect('/blog/')
        else:
            return render(request, 'login.html', {'error_message': "Invalid Credentials"})
    return render(request, 'login.html')
def checkUsername(request):
    username = request.GET['username']
    if User.objects.filter(username = username).exists():
        return HttpResponse("exists")
    else:
        return HttpResponse("not_exist")
@login_required
def blog(request):
    user_article = article.objects.filter(user = request.user)
    return render(request, 'blog.html', {'user_article':user_article})
@login_required
def privacy(request,article_id):
    try:
        art = article.objects.get(id = article_id)
    except article.DoesNotExist:
        raise Http404("Article does not exist")
    if art.private:
        art.private = False
        art.save()
        return HttpResponse("was_private")
    else:
        art.private = True
        art.save()
        return HttpResponse("was_not_private")
@login_required
def userView(request):
    uname = request.GET['username']
    if uname.rstrip() == "":
        return HttpResponse("blank")
    all_user = User.objects.filter(username__contains= uname)
    data = []
    for user in all_user:
        ser = CurrentUserSerializer(user)
        data.append(ser.data)
    return HttpResponse(json.dumps(data))
@login_required
def userDetail(request,user_id):
    try:
        ourUser = User.objects.get(id = user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    all_article = article.objects.filter( user = ourUser,private = False )
    return render(request,'other.html',{'user_article':all_article,'ourUser':ourUser})
@login_required
def add(request):
    message = None
    if 'addPost' in request.POST:
        private = False
        title = request.POST['title']
        if 'private' in request.POST:
            private = bool(request.POST['private'])
        description = request.POST['description']
        arti = article(user = request.user, title = title, description = description, private = private)
        arti.save()
        if 'image' in request.FILES:
            my_image = request.FILES['image']
            arti.image = my_image
            arti.save()
        message = "Article Added sucessfully"
    return render(request,'add.html',{'message':message})
@login_required
def fullArticle(request,article_id):
    try:
        art = article.objects.get(id =article_id)
    except article.DoesNotExist:
        raise Http404("Aricle does not exists")
    if request.user == art.user or art.private == False:
        return render(request,'detail.html',{'article':art})
    else:
        raise Http404("Unathorized acess.This is a security feature added. Only private and self article can be viewed")
    

