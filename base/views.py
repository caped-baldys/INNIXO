import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.test import TestCase
from .models import User, Event, Submission, Comment , EventRegistration
from .forms import SubmissionForm, CustomUserCreateForm, UserForm , EventRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from PIL import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage 
import os
# from settings import MEDIA_ROOT
# Create your views here.

def login_page(request):
    page = 'login'

    if request.method == "POST":
        user = authenticate(
            email=request.POST['email'],
            password=request.POST['password']
            )

        if user is not None:
            login(request, user)
            messages.info(request, 'You have succesfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Email OR Password is incorrect')
            return redirect('login')
    
    context = {'page':page}
    return render(request, 'login_register.html', context)

def register_page(request):
    form = CustomUserCreateForm()

    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST, request.FILES,)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, 'User account was created!')
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')


    page = 'register'
    context = {'page':page, 'form':form}
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def home_page(request):
    limit = request.GET.get('limit')

    if limit == None:
        limit = 20

    limit = int(limit)

    users = User.objects.filter(hackathon_participant=True)
    count = users.count()

    page = request.GET.get('page')
    paginator = Paginator(users, 50)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)


    pages = list(range(1, (paginator.num_pages + 1)))
 

    
    events = Event.objects.all()
    context = {'users':users, 'events':events, 'count':count, 'paginator':paginator, 'pages':pages}
    return render(request, 'home.html', context)


def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'profile.html', context)

@login_required(login_url='/login')
def account_page(request):
    user = request.user

    # img = user.avatar
    # img = Image.open(user.avatar)
    # newsize = (10, 10)
    # img = img.resize(newsize)
  
    # user.avatar = img
    # user.save()
    # user.save()

    context = {'user':user}
    return render(request, 'account.html', context)

@login_required(login_url='/login')
def edit_account(request):
    
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        print(form)
        form = UserForm(request.POST, request.FILES,  instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'user_form.html', context)

@login_required(login_url='/login')
def change_password(request):   
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
       
        if password1 == password2:
             new_pass = make_password(password1)
             request.user.password = new_pass
             request.user.save()
             messages.success(request, 'You have succesfully reset your password!')
             return redirect('account')

    return render(request, 'change_password.html')


import time
from datetime import datetime
#For upload file path

def get_custom_file_path(instance, filename):
    # Extract the extension from the original file name
    extension = filename.split('.')[-1]
    
    # Construct the new filename using the user's username
    new_filename = f"{instance.teamleader.username}.{extension}"
    
    # Create a directory path for the event name (replace spaces with underscores for better compatibility)
    event_name_safe = instance.event.name.replace(' ', '_')
    upload_dir = os.path.join(settings.UPLOADS_ROOT, event_name_safe)
    
    # Combine the new path and filename
    custom_path = os.path.join(upload_dir, new_filename)
    return custom_path




@login_required(login_url='/login')
def registration_confirmation(request, pk):
    
    event = Event.objects.get(id=pk)
    max_members = range(1, event.max_members + 1)
    min_members = event.min_members
    if request.method == 'POST':
        # Process the form data
        try:
            max_members = range(1, event.max_members + 1)
            min_members = event.min_members
            # teamleader_id = request.user
            teamleader = request.user
            # Create a temporary instance to use in get_custom_file_path
            temp_instance = EventRegistration(event=Event.objects.get(id=pk), teamleader=teamleader)
            # temp_instance = f'{event.name}{request.user}'
            team_name = request.POST.get('team_name')
            phone_number = request.POST.get('phone_number')

            payment_image = request.FILES.get('payment') if 'payment' in request.FILES else None

            if payment_image:
                            fs = FileSystemStorage()
                            custom_path = get_custom_file_path(temp_instance, payment_image.name)
                            # Save the file to the FileSystem
                            filename = fs.save(custom_path, payment_image)
                            uploaded_file_url = fs.url(filename)
            else:
                uploaded_file_url = None

            registration = EventRegistration(
                event=event,
                teamleader=request.user,
                team_name=team_name,
                phone_number=phone_number,
                memeber_1=request.POST.get('memeber_1'),
                memeber_2=request.POST.get('memeber_2'),
                memeber_3=request.POST.get('memeber_3'),
                memeber_4=request.POST.get('memeber_4'),
                memeber_5=request.POST.get('memeber_5'),
                payment=uploaded_file_url,
            )
            
            # Assuming you validate the phone number and other field    s as needed
            registration.full_clean()
            registration.save()
            messages.info(request, 'You have registered for ' + event.name)
            return redirect('home')
        except ValidationError as e:
            # Handle errors and validation issues
            print(e)
            return render(request, 'event_confirmation.html', {'error': e.message_dict, 'event': event,'max_members': max_members,'min_members':min_members})
        except Exception as e:
            print(e)
            # error handling
            return render(request, 'event_confirmation.html', {'error': str(e), 'event': event,'max_members': max_members,'min_members':min_members})
    else:
        # GET request, show the empty form
        print('some error')
        return render(request, 'event_confirmation.html', {'event': event, 'max_members': max_members,'min_members':min_members})

    return render(request, 'event_confirmation.html', {'event':event,'form':form})

@login_required(login_url='/login')
def project_submission(request, pk):
    event = Event.objects.get(id=pk)

    form = SubmissionForm()

    if request.method == 'POST':
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            
            return redirect('account')

    context = {'event':event, 'form':form}
    return render(request, 'submit_form.html', context)


#Add owner authentication
@login_required(login_url='/login')
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse('You cant be here!!!!')

    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')


    context = {'form':form, 'event':event}

    return render(request, 'submit_form.html', context)

@login_required(login_url='/login')
def deleteMessage(request):

    # form = RoomForm(instance=room)
    # context = {'form':form}
    if request.method == 'POST':
        message = Comment.objects.get(id=request.POST['Id'])
        if request.user != message.user:
            return HttpResponse('ERROR!')
        message.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def event_page(request, pk):
    event = Event.objects.get(id=pk)
    comments = event.comment_set.all()
    # print('image:',event.image.url)
    
    registered = False
    submitted = False
    
    if request.user.is_authenticated:

        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()

    if request.method == 'POST':
        message = Comment.objects.create(
            user=request.user,
            event=event,
            body=request.POST.get('body')
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'event':event, 'registered':registered, 'submitted':submitted, 'comments':comments}
    return render(request,'event-new.html',context)

#404 handler
def error_404_view(request, exception):
   
    return render(request, '404.html')