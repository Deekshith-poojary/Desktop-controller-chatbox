from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
import json
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
import sys,time
from django.utils import timezone

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

resp={'outp':None,'lpin':1}
cmd={'cmd':'cls','pin':1}
def chatbot(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        cmd['cmd']=message
        cmd['pin']+=1
        time.sleep(3)    
        if int(resp['lpin'])==int(cmd['pin']):
            response=resp['outp']
        else:
            response='Not executed'        
                
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now)
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

@csrf_exempt
def data(request):
    if request.method == 'POST':
        resp['outp'] = request.POST['output']
        resp['lpin'] = request.POST['pin']
        return JsonResponse({'status':'sucess'})
    return HttpResponse('not allowed')

@csrf_exempt
def send(request):
    if request.method == 'POST':
        return JsonResponse(cmd)

@csrf_exempt
def setup(request):
    if request.method == 'POST':
        resp['outp']=None
        resp['lpin']=1
        cmd['cmd']='cls'
        cmd['pin']=1
        return JsonResponse({'setup':1})
    return HttpResponse('not allowed')

@csrf_exempt        
def system_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({'login':1})
        else:
            return JsonResponse({'login':0})

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
            return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Password don't match" 
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')