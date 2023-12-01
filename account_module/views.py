from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
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
            otp_code = OtpCode.objects.create(user=user)
            otp_code.generate_code()
            is_sent, message = send_otp_code(otp_code=otp_code, email_address=ser_data.validated_data['email'],
                                             phone_number=ser_data.validated_data['phone_number'])
            return Response({'message': message}, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
