from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from twilio.rest import Client
import os

import uuid
import boto3

from .models import Event, Photo, Item, User
from .forms import ItemForm

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'eventus-cns'

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
# Define home view

def home(request):
  return render(request, 'home.html')

#Define about view
def about(request):
  return render(request, 'about.html')

def success(request):
  return render(request, 'success.html')

def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', { 'events': events })

@login_required
def events_detail(request, event_id):
  event = Event.objects.get(id=event_id)
  attendees_event_doesnt_have = User.objects.exclude(id__in = event.attendees.all().values_list('id'))
  item_form = ItemForm()
  return render(request, 'events/detail.html', { 'event': event, 'item_form': item_form, 'attendees': attendees_event_doesnt_have })

class EventUpdate(LoginRequiredMixin, UpdateView):
  model = Event
  fields = ['name', 'what', 'date', 'where', 'why', 'organizer']
  success_url = '/events/'

class EventDelete(LoginRequiredMixin, DeleteView):
  model = Event
  success_url = '/events/'

class EventCreate(LoginRequiredMixin, CreateView):
  model = Event
  fields = ['name', 'what', 'date', 'where', 'why', 'organizer']
  success_url = '/events/'

  def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

@login_required
def add_photo(request, event_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, event_id=event_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', event_id=event_id)

@login_required
def add_item(request, event_id):
  form = ItemForm(request.POST)
  if form.is_valid():
    new_item = form.save(commit=False)
    new_item.event_id = event_id
    new_item.save()
  return redirect('detail', event_id=event_id)

class AttendeesList(ListView):
    model = User
    fields = '__all__'

def assoc_user(request, event_id, user_id):
    Event.objects.get(id=event_id).attendees.add(user_id)
    return redirect('detail', event_id=event_id)

# def get_item_from_request(request):
#     print(request.POST)
#     return the_item

# def delete_post(request):
#     the_post = get_post_from_request(request)
#     if request.user == the_post.User:
#         the_post.delete()
#         return http.HttpResponseRedirect("/your/success/url/")
#     else:
#         return http.HttpResponseForbidden("Cannot delete other's posts")

def run_sms(request):
  
  account_sid = os.environ['ACCOUNT_SID']
  auth_token = os.environ['AUTH_TOKEN']
  client = Client(account_sid, auth_token)
  phoneadj = "+1" + request.user.userprofile.phone
  message = client.messages \
    .create(
         body= 'OMFG IT WORKED!',
         from_='+18705222095',
         to= phoneadj
     )
  print(message.sid)
  return redirect('success')
