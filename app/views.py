from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AuthUser , UserFriend
from datetime import datetime
from app import serviceMail
from random import randint

# Create your views here.

def login_us(request):
    return render(request, 'login.html')

@login_required(login_url='')
def index(request):
    data = {}
    data['user'] = []
    data['users'] = []
    data['user'].append(request.user)
    data['friends'] = UserFriend.objects.filter(my_id=request.user.id)
    
    if request.method == 'POST':
        var = request.POST.get('Search')
        data['users'] = AuthUser.objects.filter(username__contains=var).exclude(
            id=request.user.id).exclude(userfriend__in=data['friends'])

    return render(request, 'index.html', data)

def logout_us(request):
    print(request.user)
    logout(request)
    return redirect('/')

@csrf_protect
def logar(request):
    if request.POST:
        user = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user, password=password)
        if user is not None:
            login(request, user)
            return redirect('/index.html')
        else:
            messages.error(request,'Usuário ou senha incorreto.')
    return redirect('/')

@csrf_protect
def register(request):
    data = {}
    data['msg'] = [] #verificar
    if request.method == 'POST':
        username = request.POST.get('username')
        firstName = request.POST.get('firstname')
        lastName = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatpassword = request.POST.get('repeatpassword')
        is_superuser = False
        is_staff = True
        is_active = True
        date_joined = datetime.now()
        try:
            val_username = User.objects.filter(username=username)
            val_email = User.objects.filter(email=email)
            if (len(val_username) > 0):
                data['msg'].append('Usuário já cadastrado!')
                return render(request, 'register.html', data)
            if (len(val_email) > 0):
                data['msg'].append('E-mail já cadastrado!')
                return render(request, 'register.html', data)
        except:
            data['msg'].append('Erro ao verificar usuário/email!')
            return render(request, 'register.html', data)
        
        if (password != repeatpassword):
            data['msg'].append('Senhas não conferem')
            return render(request,'register.html', data)
        try:
            user = User(is_superuser=is_superuser,
            username=username,
            first_name=firstName,
            last_name=lastName,
            email=email,
            is_staff=is_staff,
            is_active=is_active,
            date_joined=date_joined)
            user.set_password(password)
            user.save()
            data['msg'].append('Cadastro realizado com Sucesso!')
            return render(request, 'login.html', data)
        except:
            data['msg'].append('Ocorreu algum erro')
            return render(request,'register.html', data)
    else:
        return render(request, 'register.html', data)
    return render(request, 'register.html')

@csrf_protect
def recuperar_senha(request):
    data = {}
    data['msg'] = []
    data['error'] = []
    if request.method == 'POST':
        email = request.POST.get('email')
        try: 
            if(email == ''):
                data['error'].append('e-mail inválido')
            else:
                val_user = User.objects.filter(email=email)
                if(len(val_user) > 0):
                    newpass = randint(10000000,99999999)
                    user = User.objects.get(email=email)
                    user.set_password(newpass)
                    user.save()
                    serviceMail.recoveryPass(newpass, user.username, email)
                    data['msg'].append('Sua nova senha foi enviada no email!')
                else:
                    data['error'].append('email não cadastrado!')
        except:
            data['error'].append('Ocorreu algum erro, tente novamente mais tarde!')
            return render(request,'recuperar_senha.html', data)
    return render(request, 'recuperar_senha.html', data)

@csrf_protect
def friend(request):
    data = {}
    data['error'] = []
    if request.method == 'GET':
        id = request.GET.get('id')
        op = request.GET.get('op')
        if(id != None and op != None):
            try:           
                friend = AuthUser.objects.get(id=id)
                iduser = int(request.user.id)
                if(friend == ''):
                    data['error'].append('Amigo inválido')
                elif(op == "add"):
                    fr = UserFriend(my_id=iduser,friend_id=friend)
                    fr.save()
                elif(op == "del"):
                    fr = UserFriend.objects.get(my_id=iduser,friend_id=friend)
                    fr.delete()
            except:
                data['error'].append("Erro ao adicionar! Tente outra vez!!!")
        return redirect('index')