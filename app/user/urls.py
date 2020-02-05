from django.urls import path

from user import views

app_name = 'user'


urlpatterns = [
	
	path('create/', views.CreateUser.as_view(), name='create'),
	path('token/', views.TokenGeneration.as_view(), name='token'),
	path('me/', views.ManagingUser.as_view(), name='me'),
] 