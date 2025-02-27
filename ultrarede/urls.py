from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.posts, name='posts'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<int:id>', views.perfil, name='perfil'),
    path('description/', views.description, name='description'),
    path('change_description/', views.change_description, name='change_description'),
    path('search/', views.search, name='search'),
    path('picture/', views.picture, name='picture'),
    path('change_picture/', views.change_picture, name='change_picture'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('exclude/<str:model>/<int:id>', views.exclude, name='exclude')
]