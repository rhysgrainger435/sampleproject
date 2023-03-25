from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()
    query = request.GET.get('q')
    if query:
        rooms = Room.objects.filter(name__icontains=query)
    else:
        rooms = Room.objects.all()
    context = {'rooms': rooms, 'query': query}

    return render(request, 'room/rooms.html', context)

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)

    return render(request, 'room/room.html', {'room': room, 'messages': messages})