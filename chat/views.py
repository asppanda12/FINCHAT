from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# Create your views here.
def home(request):
    
       url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
       parameters = {
                 'start':'1',
                 'limit':'10',
                 'convert':'INR'
                  }
       headers = {
         'Accepts': 'application/json',
         'X-CMC_PRO_API_KEY': 'b8929fe4-d1e0-454b-8d1d-772071b24abd',
       }

       session = Session()
       session.headers.update(headers)
       try:
           response = session.get(url, params=parameters)
           data1 = json.loads(response.text)
           coins = data1['data']
           p=0 
           pupils_dictionary = {}
           for x in coins:
               new_key =p
               fruits = [x['symbol'], x['quote']['INR']['price']]
               new_age =fruits
               pupils_dictionary[new_key] = new_age
               p=p+1
               print( pupils_dictionary)
       except (ConnectionError, Timeout, TooManyRedirects) as e:
             print(e)
       return render(request, 'home.html',{'data1':pupils_dictionary,'n' : range(6) })

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})