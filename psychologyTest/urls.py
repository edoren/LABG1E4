from django.conf.urls import url
from psychologyTest import views

urlpatterns = [
    url(r"^$", views.login_page, name="login_page"),
    url(r"^logout", views.logout_page, name="logout_page"),
    url(r"^home_admin", views.home_admin, name="home_admin"),
    url(r"^home_psychologist", views.home_psychologist, name="home_psychologist"),
    url(r"^home_student", views.home_student, name="home_student"),
    url(r"^register", views.register, name="register"),
    url(r"^restore_password", views.restore_password, name="restore_password"),
    # url(r"^manage_users", views.manage_users, name="manage_users"),
    url(r"^account_requests", views.account_requests, name="account_requests"),
    url(r"^manage_groups", views.manage_groups, name="manage_groups"),
    url(r"^manage_institutions", views.manage_institutions,
        name="manage_institutions"),
    url(r"^edit_profile", views.edit_profile,
        name="edit_profile"),
]
