from django.urls import path
from . import views

urlpatterns = [
    path('login/',                              views.login_view,      name='login'),
    path('logout/',                             views.logout_view,     name='logout'),
    path('registo/',                            views.registo_view,    name='registo'),
    path('magic/<int:user_pk>/<str:token>/',   views.magic_link_view, name='magic_link'),
]