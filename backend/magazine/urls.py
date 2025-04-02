from django.urls import path
from . import views
from .views import QuizListCreateView, QuizDetailView, QuestionCreateView, AnswerCreateView, QuestionDetailView,AnswerDetailView,RegisterView, QuizUpdateView, QuizDeleteView,NewsCountView, DiscussionListCreateView, DiscussionDetailView


urlpatterns = [
    path('api/login', views.LoginView.as_view(), name='login'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/news/', views.NewsList.as_view(), name='news-list'),
    path('api/news_general/', views.NewsGeneral.as_view(), name='news-general-list'),
    path('api/news_it/', views.NewsIT.as_view(), name='news-it-list'),
    path('api/news_type/', views.NewsType.as_view(), name='news-type-list'),
    path('api/news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news-edit'),
    path('api/news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news-delete'),
    path('api/author/', views.getAuthors.as_view(), name='author'),
    path('latest-news/', views.LatestNewsView.as_view(), name='latest-news'),
    path('latest-news1/', views.LatestNewsViews.as_view(), name='latest-news-views'),
    path('api/news_count/', NewsCountView.as_view(), name='news-count'),

    
    path("api/quiz/", QuizListCreateView.as_view(), name="quiz-list"),
    path("api/quiz/<int:pk>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("api/quiz/<int:quiz_id>/questions/", QuestionCreateView.as_view(), name="question-create"),
    path("api/questions/<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),
    path("api/questions/<int:question_id>/answers/", AnswerCreateView.as_view(), name="answer-create"),
    path("api/answers/<int:pk>/", AnswerDetailView.as_view(), name="answer-detail"),
    
    path('api/discussions/', DiscussionListCreateView.as_view(), name='discussion-list-create'),
    path('api/discussions/<int:pk>/', DiscussionDetailView.as_view(), name='discussion-detail'),
]
