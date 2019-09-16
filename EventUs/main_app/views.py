from django.shortcuts import render
from .models import Event
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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