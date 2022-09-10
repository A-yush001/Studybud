from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Q


from django.http import HttpResponse 
from .models import Room ,Topic ,Message,User
from .forms import RoomForm,Userform,MyUserCreationform

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def loginpage(request):
    page='login'
   


    if request.method=='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')

       

        user=authenticate(request,email=email , password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
            

    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registeruser(request):
     
    f = MyUserCreationform()
    if request.method == 'POST':
        f = MyUserCreationform(request.POST)
        if f.is_valid():
            user=f.save(commit=False)
            user.username=user.username.lower()
            messages.success(request, 'Account created successfully')
            user.save()
            login(request,user)
            return redirect('home')

        else:
             messages.error(request, 'An error occured during registration')

            
    return render(request,'base/login_register.html',{'form':f})
    




def home(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ""
    rooms=Room.objects.filter(Q(topic__name__contains=q)|Q(name__contains=q)|Q(description__contains=q))
    topic=Topic.objects.all()[0:5]
    room_count=rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__contains=q))
    context ={'rooms':rooms,'topics':topic,'room_count':room_count,"room_messages":room_messages}
    return  render(request,"base/home.html",context)

    
def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=="POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={"room":room,"room_messages": room_messages,"participants":participants}

    return  render(request,"base/room.html",context)


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={"user":user,"rooms":rooms,"room_messages":room_message,"topics":topics}
    return render(request,"base/profile.html",context)

@login_required(login_url='login')
def createroom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')

       
           
    context={'form':form,"topics":topics}
    return render(request,"base/room_form.html",context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('name')
        room.save()
        
        return redirect('home')
    context={'form':form,"topics":topics,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method=="POST":
        room.delete()
        return redirect('home')
    
    return render(request,"base/delete.html",{'obj':room})



@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    if request.method=="POST":
        message.delete()
        return redirect('home')
    
    return render(request,"base/delete.html",{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=Userform(instance=user)
    if request.method=='POST':
        form=Userform(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    

    return render(request,"base/update_user.html",{'form':form})

def topicspage(request):
    q= request.GET.get('q') if request.GET.get('q')!=None else ""
    topics=Topic.objects.filter(name__contains=q)
    return render(request,"base/topics.html",{'topics':topics})


def activitypage(request):
    room_messages=Message.objects.all()
    return render(request,"base/activity.html",{'room_messages':room_messages})