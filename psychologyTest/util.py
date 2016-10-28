from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from psychologyTest.models import User


def RedirectToHome(user):
    rol_homes = {
        "R": "/admin",
        "A": "home_admin",
        "P": "home_psychologist",
        "S": "home_student"
    }
    view = rol_homes.get(user.role, None)
    return redirect(view)
