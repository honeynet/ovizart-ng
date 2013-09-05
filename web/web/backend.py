__author__ = 'ggercek'
import sys
import os
d = os.path.abspath(__file__)
dirname = os.path.dirname(d)
sys.path.append(os.path.join(dirname, '../../'))  # PROJECT_ROOT

from django.contrib.auth.models import User, check_password

from core.ovizart_proxy import OvizartProxy


class OvizartUser(User):

    def __init__(self, *args, **kwargs):
        User.__init__(self, args, kwargs)
        self.ovizart = kwargs['ovizart']

user_cache = {}


class OvizartAuthenticationBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """

    def authenticate(self, username=None, password=None, protocol='http', host='localhost', port=9009):
        global user_cache
        user = None
        op = OvizartProxy(protocol, host, port)

        if username and password:
            response = op.login(username, password)
            if response['Status'] == 'OK':
                userid = response['userid']
                user = User(username=username, pk=userid)
                user.is_staff = True
                user.is_superuser = True
                user.__dict__['ovizart'] = op
                user_cache[userid] = user
                user.save()

        return user

    def get_user(self, user_id):
        global user_cache
        try:
            return user_cache[user_id]
        except User.DoesNotExist:
            return None