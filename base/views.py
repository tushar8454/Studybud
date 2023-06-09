from django.shortcuts import render,redirect

# if you send http req. first import HttpResponse
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm,UserForm
#WE USE FOR LOGIN PAGE
from django.contrib.auth.models import User
#for flash message to the user
from django.contrib import messages
#it is user for login and logout for user
from django.contrib.auth import authenticate,login,logout
#it is use for restricted the page to logout user
from django.contrib.auth.decorators import login_required
#it is use for making just like login form and signup
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
 
# Create your views here.


# rooms=[
#     {'id':1,'name':'lets learn python'},
#      {'id':2,'name':'Design with me'},
#       {'id':3,'name':'frontend devloper'},

# ]

def loginpage(request):

    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
        #we check user is present is db or not
           user=User.objects.get(username=username)
        except:
            messages.error(request,'user does not exist')

        user=authenticate(request,username=username,password=password)

        if user is not None:
                login(request,user)
                return redirect('home')
        else:
                messages.error(request,'username or password does not exits')   


    context={'page':page}
    return render(request,'base\login_view.html',context)


def logoutuser(request):
    #it is method to delete a token which user is login
    logout(request)
    return redirect('home')


def registerpage(request):
   
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm()
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error ocured during registration')    

           
    return render(request,'base/login_view.html',{'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
  #topic_name_icontains is used for filter the ojects in model
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    # return HttpResponse('home page')
    topics=Topic.objects.all()
    room_count=rooms.count()
    room_messages=Message.objects.filter(
        Q(room__topic__name__icontains=q))

    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    
    return render(request,'base/home.html',context)


def room(request,pk):
    # room=None
    # for i in rooms:
    #     if i[id]==int(pk):
    #         room=i
    # context={'room':room}
    # return HttpResponse('room')
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    # room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    
    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')

        )
        room.participants.add(request.user)

        return redirect('room',pk=room.id)


    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)


def userprofile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


#it work when the user is not identified it is redirect to login
@login_required(login_url='login')
def createroom(request):
   form=RoomForm()
   topics=Topic.objects.all()

   if request.method == 'POST':
    topic_name=request.POST.get('topic')
    topic, created = Topic.objects.get_or_create(name=topic_name)

    Room.objects.create(
        host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
    )
    return redirect('home')

#    ---- it is old method to save the form----
    # form=RoomForm(request.POST)
    # if form.is_valid():
    #     room=form.save(commit=False)
    #     room.host=request.user
    #     room.save()
        # return redirect('home')

   context={'form':form,'topics':topics}
   return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()

    if request.user!=room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method=='POST':
        topic_name=request.POST.get('Topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form=RoomForm(request.POST,instance=room)
        room.name=request.POST.get('name')
        room.topic=topic
        room.discription=request.POST.get('discription')
        room.save()
        return redirect('home')

    context={'form':form,'topics':topics,'rooms':room}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('Your are not allowed here!!')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deletemessage(request,pk):
    message=Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})   


@login_required(login_url='login')
def updateuser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method == 'POST':
        form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    
    return render(request,'base/update-user.html',{'form':form})
