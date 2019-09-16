from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import uuid
import boto3

from .models import Event, Photo

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
  return render(request, 'events/detail.html', { 'event': event })

class EventUpdate(UpdateView):
  model = Event
  fields = ['name', 'what', 'where', 'why', 'organizer']

class EventDelete(DeleteView):
  model = Event
  success_url = '/events/'

class EventCreate(CreateView):
  model = Event
  fields = ['name', 'what', 'where', 'why', 'organizer']
  success_url = '/events/'

