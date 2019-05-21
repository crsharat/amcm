from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class SimpleAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        user = super().new_user(request)
        user.is_staff = True
        return user

class AutoSignupAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        try:
            email = sociallogin.account.extra_data.get('email')
            verified = sociallogin.account.extra_data.get('verified_email')
            if email and verified:
                user = User.objects.get(email=email)
                if not sociallogin.is_existing:
                    sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass