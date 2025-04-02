
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import News,Quiz,Question,Answer
from .serializers import NewsListSerializer,NewsPostSerialzier,QuizSerializer, QuestionSerializer, AnswerSerializer
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny 
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Discussion
from .serializers import DiscussionSerializer
from rest_framework.permissions import AllowAny
from django.db.models import Count

from django.core.cache import cache

#Discussion

class DiscussionListCreateView(APIView):
    permission_classes = []

    def get(self, request):
        discussions = Discussion.objects.all().order_by('-created_date')
        serializer = DiscussionSerializer(discussions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DiscussionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiscussionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Discussion, pk=pk)

    def get(self, request, pk):
        discussion = self.get_object(pk)
        serializer = DiscussionSerializer(discussion)
        return Response(serializer.data)

    def put(self, request, pk):
        discussion = get_object_or_404(Discussion, pk=pk)
        serializer = DiscussionSerializer(discussion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discussion = self.get_object(pk)

        if request.user != discussion.author:
            return Response({"error": "You do not have permission to delete this discussion."}, status=status.HTTP_403_FORBIDDEN)

        discussion.delete()
        return Response({"message": "Discussion deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

#News

class NewsCountView(APIView):
    def get(self, request):
        year = int(request.query_params.get("year", datetime.now().year))
        quarter = int(request.query_params.get("quarter", 1))

        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2

        start_date = datetime(year, start_month, 1).date()
        if end_month == 12:
            end_date = datetime(year, 12, 31).date()
        else:
            end_date = datetime(year, end_month + 1, 1).date()

        total_news_count = News.objects.filter(created_date__gte=start_date, created_date__lt=end_date).count()
        type_1_count = News.objects.filter(type="1", created_date__gte=start_date, created_date__lt=end_date).count()
        type_2_count = News.objects.filter(type="2", created_date__gte=start_date, created_date__lt=end_date).count()

        return Response({
            "total_news_count": total_news_count,
            "type_1_count": type_1_count,
            "type_2_count": type_2_count,
        }, status=status.HTTP_200_OK)


#Quiz

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
class QuizUpdateView(generics.UpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = []

class QuizDeleteView(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    permission_classes = []
    
class QuizDetailView(APIView):
    def get(self, request, pk):
        try:
            quiz = Quiz.objects.get(id=pk)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            quiz = Quiz.objects.get(id=pk)
            serializer = QuizSerializer(quiz, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            quiz = Quiz.objects.get(id=pk)
            quiz.delete()
            return Response({"message": "Quiz deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

class QuestionCreateView(APIView):
    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(data={"quiz": quiz.id, **request.data})
        if serializer.is_valid():
            question = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetailView(APIView):
    def put(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return Response({"message": "Question deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class AnswerCreateView(APIView):
    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)  

        data = request.data.copy()
        data["question"] = question.id  

  
        if data.get("is_correct") and Answer.objects.filter(question=question, is_correct=True).exists():
            return Response({"error": "Only one correct answer is allowed per question."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnswerDetailView(APIView):
    def put(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = AnswerSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        answer.delete()
        return Response({"message": "Answer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


#Register 

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'required': False},  # Allow optional superuser field
        }

    def create(self, validated_data):
        is_superuser = validated_data.pop('is_superuser', False)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
        return user



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsList(APIView):
    permission_classes = [AllowAny]
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get(self, request):
        news = News.objects.all().order_by('-created_date')
        serializer = NewsListSerializer(news, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request): 
        data = request.data.copy()
        data["author"] = request.user.id 
        serializer = NewsPostSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsIT(APIView):
    permission_classes = [AllowAny]
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get(self, request):
        news = News.objects.filter(type=1)
        serializer = NewsListSerializer(news, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class NewsGeneral(APIView):
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get(self, request):
        news = News.objects.filter(type=2)
        serializer = NewsListSerializer(news, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class NewsType(APIView):
    def get(self,request):
        news_types = [{"value": value, "label": label} for value, label in News.TYPES]
        return JsonResponse(news_types, safe=False)
    
class getAuthors(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        authors=User.objects.filter(is_superuser=True).values('id','username')
        
    
        return JsonResponse(list(authors),safe=False)

class NewsUpdateView(APIView):
    permission_classes = []

    def put(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        
        if request.user != news.author and not request.user.is_superuser:
            return Response({"error": "You do not have permission to edit this news."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = NewsPostSerialzier(news, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # After updating, return the updated news list
            news_list = News.objects.all()
            news_serializer = NewsListSerializer(news_list, many=True)
            return Response({
                "updated_news": serializer.data,
                "news_list": news_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDeleteView(APIView):
    permission_classes = []

    def delete(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        
        if request.user != news.author and not request.user.is_superuser:
            return Response({"error": "You do not have permission to delete this news."}, status=status.HTTP_403_FORBIDDEN)
        
        news.delete()
        
        # After deleting, return the updated news list
        news_list = News.objects.all()
        news_serializer = NewsListSerializer(news_list, many=True)
        return Response({
            "message": "News deleted successfully",
            "news_list": news_serializer.data
        }, status=status.HTTP_204_NO_CONTENT)

  
class LoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            if User.objects.filter(username=username).exists():
                return Response({"detail": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"detail": "Username not found."}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Account is inactive."}, status=status.HTTP_400_BAD_REQUEST)
class LatestNewsView(generics.ListAPIView):
    queryset = News.objects.filter(type=2).order_by('-created_date')[:1]  # Get the latest news
    serializer_class = NewsListSerializer
class LatestNewsViews(generics.ListAPIView):
    queryset = News.objects.filter(type=1).order_by('-created_date')[:1]  # Get the latest news
    serializer_class = NewsListSerializer
    

    