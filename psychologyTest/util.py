from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from psychologyTest.models import User


def RedirectToHome(user):
    rol_homes = {
        "A": "home_admin",
        "P": "home_psicologist",
        "S": "home_student"
    }
    view = rol_homes.get(user.role, None)
    return HttpResponseRedirect(reverse(view))
