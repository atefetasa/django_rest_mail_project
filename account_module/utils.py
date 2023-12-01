from kavenegar import *
from django.template.loader import render_to_string
from django.core.mail import send_mail
import re


def send_sms(to, message):
    api = KavenegarAPI('5435686B554A48676B434F3072395962714B666C395049306337305336394F59714B4976316D54684B42773D')
    try:
        params = {
            'sender': '1000689696',
            'receptor': to,
            'message': message,
        }
        api.sms_send(params)
        return True
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def create_pattern(raw_string):
    pattern = rf'\b{re.escape(raw_string)}|\b{re.escape(raw_string)}\b'
    return re.compile(pattern)


def send_otp_code(otp_code, email_address, phone_number):
    is_sent = False
    message = ""
    if email_address:
        html_message = render_to_string('account_module/activation_email.html', {'otp': otp_code.code})
        success_count = send_mail(subject='account activation', message='', from_email='atenafallahi14@gmail.com',
                                  recipient_list=[email_address], html_message=html_message)
        if success_count == 1:
            otp_code.is_used = True
            is_sent = True
            message = 'you have been registered into the system and ' \
                      'the activation code has been successfully sent to your email'
        elif success_count == 0:
            otp_code.is_used = False
            is_sent = False
            message = 'you have been registered into the system ' \
                      'but the activation code has not been sent successfully'

    if phone_number:
        to = phone_number
        sms_message = f"""
                    this is your account activation code
                    this code is valid only for 4 minutes
                    activation code: {otp_code.code}
                    please enter it to activate your account 
                """
        result = send_sms(to=to, message=sms_message)
        if result:
            otp_code.is_used = True
            is_sent = True
            message = 'you have been registered into the system and ' \
                      'activation code has been successfully sent as a text message to your phone'
        else:
            is_sent = False
            message = 'you have been registered into the system ' \
                      'but the activation code has not been sent successfully'

    otp_code.save()
    return is_sent, message
