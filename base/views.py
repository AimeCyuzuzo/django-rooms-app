import email
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from matplotlib.style import context
from .models import Message, Room, Topic, Profile
from .forms import RoomForm, UpdateUserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm




# rooms = [
#     {
#         'id': 1,
#         'name': 'Python learning'
#     },
#     {
#         'id': 2,
#         'name': "English group"
#     }
# ]



def login_page(request):

    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")

    if request.user.is_authenticated:
        return redirect('home')

    context = {'page': page}
    return render(request, 'base/login-register.html', context)


def signup_page(request):
    page = 'signup'
    form = UserCreationForm

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        othernames = request.POST.get('othernames')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        profilePicture = request.POST.get('profile')
        bio = request.POST.get('bio')
        email = request.POST.get('email')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower();
            user.save()
            profile = Profile.objects.create(
                owner = user,
                profilePicture = profilePicture,
                bio = bio,
                firstname = firstname,
                othernames = othernames,
                gender = gender,
                age = age,
                email = email
            )

            login(request,user)
            return redirect('login')
        else:
            messages.error(request, ("An error occurred. Please try again!"))


    context = {'page': page, 'form': form}
    return render(request, 'base/login-register.html', context)





def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) |
        Q(host__username__icontains = q)
    )

    # ver_user = request.user
    if request.user.is_authenticated:
        ver_profile = Profile.objects.all()
        temp_array = []
        temp_array.append(ver_profile)
        print(temp_array)
    
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q) | Q(room__topic__name__icontains=q)| Q(user__username__icontains=q)).order_by('-created')
    room_messages = room_messages[0:4]

    topics = Topic.objects.all()
    context = {
        'rooms':rooms, 'topics': topics, 'room_count': room_count,
        'room_messages': room_messages
        }
    return render(request, 'base/home.html', context)


def room(request, id):

    # room = None
    # for r in rooms:
    #     if r['id'] == int(id):
    #         room = r

    room = Room.objects.get(id=id)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        room_message = Message.objects.create(
            user = request.user,
            room= room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',id=room.id)

    
    context = {
        'room':room, 'room_messages': room_messages, 'participants':participants
        }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        

        room = Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            
        )
        room.participants.add(request.user)
        return redirect('home')



        # if form.is_valid():

        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')
    context = {'form': form}
    return render(request, 'base/room-form.html', context)


@login_required(login_url='login')
def update_room(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user  != room.host:
        return HttpResponse("You are not allowed to edit this room.")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room-form.html', context)

@login_required(login_url='login')
def delete_room(request, id):
    room = Room.objects.get(id = id)

    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this room.")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete-object.html', context)



@login_required(login_url='login')
def delete_message(request, id):
    message = Message.objects.get(id = id)

    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this message.")

    if request.method == 'POST':
        message.delete()
        return redirect('room' + message.room.objects.get(id))
    context = {'obj': message}
    return render(request, 'base/delete-object.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')


def user_profile(request, username):
    user = User.objects.get(username=username)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'room_messages':room_messages,'user':user, 'rooms':rooms,'topics':topics
        }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def update_user(request):
    form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
                request.user.profile.profilePicture = request.POST.get('profilepic')
                request.user.profile.bio = request.POST.get('bio')
                form.save()
                return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Invalid form")
    else:
        messages.error(request, "Unable to establish secure request!")
    context = {'form':form}
    return render(request, 'base/update-user.html', context)











