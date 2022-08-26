# this file is created to send an activation code, when a user account
# is created

from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    # creating a link that be used to activate the account
    # the activation code will be embedded into the link
    activation_url = f'http://localhost:8000/registration/activate/{activation_code}'
    message = f'Thank you for signing up. Please activate your account.' \
              f'Pleas follow the link below: {activation_url}'
    send_mail('Activate your account',
              message,
              'registration@admin.com',
              [email, ],
              fail_silently=False
              )
