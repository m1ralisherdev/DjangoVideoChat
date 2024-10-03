from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt


def lobby(request):
    return render(request, 'base/lobby.html')


def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "c46f544d669e47d6b08d3f39f7d7418a"
    appCertificate = "7d5c48553f89400fbb53a7d922963eeb"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    room_name = data['room_name']
    uid = data['UID']
    name = data['name']

    # Xonadagi foydalanuvchilar sonini tekshirish
    current_members_count = RoomMember.objects.filter(room_name=room_name).count()

    if current_members_count >= 2:
        return JsonResponse({'error': 'Room is full. Please try again later.'}, status=400)

    # Yangi a'zoni yaratish
    member, created = RoomMember.objects.get_or_create(
        name=name,
        uid=uid,
        room_name=room_name
    )

    return JsonResponse({'name': name}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    try:
        member = RoomMember.objects.get(uid=uid, room_name=room_name)
        return JsonResponse({'name': member.name}, safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    try:
        member = RoomMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse({'message': 'Member deleted'}, safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)


def getRoomStatus(request):
    room_name = request.GET.get('room_name')
    current_members_count = RoomMember.objects.filter(room_name=room_name).count()

    if current_members_count >= 2:
        return JsonResponse({'status': 'full'}, status=200)

    return JsonResponse({'status': 'available'}, status=200)
