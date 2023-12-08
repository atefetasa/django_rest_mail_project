from rest_framework import serializers
from .models import User
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if (not data['email']) and (not data['phone_number']):
            raise serializers.ValidationError('you must provide either an email address or phone number')

        return data

    def validate_password2(self, value):
        password = self.initial_data['password']
        if value != password:
            raise serializers.ValidationError("password and password confirmation must match")

        return value

    def validate_username(self, value):
        numbers = re.findall("\d", value)
        if (len(value) > 30) or (len(value) < 5):
            raise serializers.ValidationError("username length should be between 5 and 30 characters")

        if len(numbers) > 4:
            raise serializers.ValidationError("your username shouldn't contain more than 4 numerical characters")

        return value

    def validate_password(self, value):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', value):
            raise serializers.ValidationError(
                "The password must contain at least 1 symbol: " + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
            )

        if not re.findall('[a-z]', value):
            raise serializers.ValidationError("The password must contain at least 1 lowercase letter, a-z.")

        if not re.findall('[A-Z]', value):
            raise serializers.ValidationError("The password must contain at least 1 uppercase letter, A-Z.")

        if not re.findall('\d', value):
            raise serializers.ValidationError("The password must contain at least 1 digit, 0-9.")

        if len(value) < 8 or len(value) > 12:
            raise serializers.ValidationError(
                "your chosen password must be between 8 and 12 characters"
            )

        return value

    def validate_phone_number(self, value):
        if value:
            phone_pattern = r"^09"
            if len(value) != 11:
                raise serializers.ValidationError("phone number should be 11 digits")

            if (not re.search(phone_pattern,value)) or (re.findall("\s", value)):
                raise serializers.ValidationError("phone number format is not correct")
        return value


class ActiveAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=6)

    def validate_entered_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("code must be completely digits.")

        return value





