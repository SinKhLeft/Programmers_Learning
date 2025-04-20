from django.urls import path, include
from .views import *

urlpatterns = [
    path('questions/', QuestionList.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question_detail'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls')),
    path('vote/', VoteList.as_view()),
    path('vote/<int:pk>/', VoteDetail.as_view())
]