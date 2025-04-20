#from rest_framework.decorators import api_view, renderer_classes
#from rest_framework.response import Response
#from django.shortcuts import render,get_object_or_404
#from rest_framework import status, mixins, generics
#from rest_framework.views import APIView

from polls.models import *
from polls_api.serializers import *
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, IsVoter
from rest_framework import status
from rest_framework.response import Response

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    #queryset = User.objects.all()
    serializer_class = RegisterSerialzier



class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)
    
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data['voter'] = request.user.id
        serializer = self.get_serializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]
    
    def perform_update(self, serializer):
        serializer.save(voter=self.request.user)
# class VoteList(generics.ListCreateAPIView):
#     serializer_class = VoteSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self, *args, **kwargs):
#         return Vote.objects.filter(voter=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(voter=self.request.user)

# class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsVoter]

# class QuestionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

#     def get(self, request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self, request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
# class QuestionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
    
#     def get(self, request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

#     def put(self, request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)

#     def delete(self, request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)
    

# class QuestionList(APIView):
#     def get(self, request):
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class QuestionDetail(APIView):
#     def get(self, request, question_id):
#         question = get_object_or_404(Question, id=question_id)
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     def put(self, request, question_id):
#         question = get_object_or_404(Question, id=question_id)
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, question_id):
#         question = get_object_or_404(Question, id=question_id)
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def QuestionListView(request):
#     if request.method == 'GET':
#         questions = Question.objects.all()
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# @api_view(['GET', 'PUT', 'DELETE'])
# def QuestionDetailView(request,question_id):
#     question = get_object_or_404(Question, id=question_id)
#     if request.method == 'GET':
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = QuestionSerializer(question, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    