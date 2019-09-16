from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

import uuid
import boto3

from .models import Event, Photo
from .forms import ItemForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'eventus-cns'

# Create your views here.

# Define home view
def home(request):
  return render(request, 'home.html')

#Define about view
def about(request):
  return render(request, 'about.html')

def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', { 'events': events })

def events_detail(request, event_id):
  event = Event.objects.get(id=event_id)
  item_form = ItemForm()
  return render(request, 'events/detail.html', { 'event': event, 'item_form': item_form })

class EventUpdate(UpdateView):
  model = Event
  fields = ['name', 'what', 'date', 'where', 'why', 'organizer']

class EventDelete(DeleteView):
  model = Event
  success_url = '/events/'

class EventCreate(CreateView):
  model = Event
  fields = ['name', 'what', 'date', 'where', 'why', 'organizer']
  success_url = '/events/'

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

def add_item(request, event_id):
  form = ItemForm(request.POST)
  if form.is_valid():
    new_item = form.save(commit=False)
    new_item.event_id = event_id
    new_item.save()
  return redirect('detail', event_id=event_id)