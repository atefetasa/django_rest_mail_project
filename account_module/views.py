from rest_framework.views import APIView
import requests
from .serializers import *
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from .models import *
from .utils import *


class UserRegisterView(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            user = ser_data.create(ser_data.validated_data)
            password_history = PasswordHistory.objects.create(user=user, password=ser_data.validated_data['password'])
            password_history.save()
            current_site = get_current_site(request)
            send_otp_url = f'http://{current_site.domain}/account/send-otp/'
            response = requests.post(send_otp_url, data={'username': user.username})
            try:
                response_dict = json.loads(response.text)
                response_text = response_dict['message']
            except json.JSONDecodeError:
                response_text = response.text

            if response.status_code == status.HTTP_200_OK:
                return Response({'message': response_text, 'user_registration_info': ser_data.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': response_text, 'user_registration_info': ser_data.data},
                                status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOtpView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        user = User.objects.filter(username__iexact=username).first()
        otp_code = OtpCode.objects.create(user=user)
        otp_code.generate_code()
        is_sent, message = send_otp_code(otp_code=otp_code, email_address=user.email,
                                         phone_number=user.phone_number)
        if is_sent:
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'message': message}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ActivateAccountView(APIView):
    def put(self, request):
        pass
