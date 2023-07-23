import random

import uuid

from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import User, Device

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        mobile_number = request.data.get('phone_number')
        if not mobile_number:
            return Response({"detail":"you should give phone number"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(phone_number=mobile_number)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=mobile_number)
        else:
            return Response({"detail Error":"this phone number already exist"}, status=status.HTTP_403_FORBIDDEN)

        device = Device.objects.create(user=user)

        code_inter = random.randint(10000, 99999)

        cache.set(str(mobile_number), code_inter, 2*60)

        return Response({"code for inter": code_inter, "time valid": "2 minute"})


class GetTokenView(APIView):
    def post(self, request):
        # karbar bayad dade haro be shekl dorost befreste
        try:
            request.data
        except:
            return Response({"detail":"please enter data according to json rules"}, status=status.HTTP_400_BAD_REQUEST)
        # karbar bayad shomare telephon ro be shekl dorost befreste
        try:
            mobile_number = request.data.get("phone_number")
            if not mobile_number:
                raise ValueError
        except:
            return Response({"detail":"you sould give phone number"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            User.objects.get(phone_number=mobile_number)
        except:
            return Response({"detail": "user with this phone number does not exist"}, status=status.HTTP_403_FORBIDDEN)
        # karbar bayad code ya faramoosh e ro be shekl dorost befreste
        try:
            forgot = request.data.get("forgot")
            code_number = request.data.get("code")
            if (not code_number and not forgot) or (code_number and forgot):
                s = "just" if forgot else ""
                return Response({"detail": "you should give %s one of code or forgot" % s}, status=status.HTTP_400_BAD_REQUEST)
            if code_number:
                raise TypeError
        except:
            code_inter = cache.get(str(mobile_number))

            if code_inter != code_number:
                return Response({"detail": "incorrect code"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            token = str(uuid.uuid4())
            return Response({"token": token})
        else:
            code_inter = random.randint(10000, 99999)
            cache.set(str(mobile_number), code_inter, 2 * 60)
            return Response({"code for inter": code_inter, "time valid": "2 minute"})





























