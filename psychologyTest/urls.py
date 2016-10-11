from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login_page, name="login_page"),
    url(r'^logout/', views.logout_page, name="logout_page"),
    url(r'^home/', views.home, name="home"),
    url(r'^register/', views.register, name="register"),
    url(r'^restore_password/', views.restore_password, name="restore_password"),
    url(r'^manage_users/', views.manage_users, name="manage_users"),
    url(r'^manage_groups/', views.manage_groups, name="manage_groups"),
    url(r'^manage_institutions/', views.manage_institutions, name="manage_institutions"),
    url(r'^edit_student_profile/', views.edit_student_profile, name="edit_student_profile"),
]
