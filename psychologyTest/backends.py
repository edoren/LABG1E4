from django.contrib.auth.backends import ModelBackend

from psychologyTest.models import User


class UserBackend(ModelBackend):

    def authenticate(self, email=None, password=None, **kwargs):
        # Some authenticators expect to authenticate by 'username'
        if email is None:
            email = kwargs.get('username')
        try:
            user = User.objects.get(email=email)
            # if user.check_password(password):
            if user.password == password:
                user.backend = "{}.{}".format(self.__module__,
                                              self.__class__.__name__)
                print user.backend
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
