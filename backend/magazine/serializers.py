# myapp/serializers.py

from rest_framework import serializers
from .models import News,Quiz, Question, Answer,Discussion
from rest_framework import generics
class NewsListSerializer(serializers.ModelSerializer):
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()
    image3 = serializers.SerializerMethodField()
    image4 = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = '__all__'  # Includes all fields

    def get_image1(self, obj):
        request = self.context.get('request')
        if obj.image1:
            return request.build_absolute_uri(obj.image1.url) if request else obj.image1.url
        return None

    def get_image2(self, obj):
        request = self.context.get('request')
        if obj.image2:
            return request.build_absolute_uri(obj.image2.url) if request else obj.image2.url
        return None
    
    def get_image3(self, obj):
        request = self.context.get('request')
        if obj.image3:
            return request.build_absolute_uri(obj.image3.url) if request else obj.image3.url
        return None
    
    def get_image4(self, obj):
        request = self.context.get('request')
        if obj.image4:
            return request.build_absolute_uri(obj.image4.url) if request else obj.image4.url
        return None
    
class NewsPostSerialzier(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'  # Includes all fields

class LatestNewsView(generics.ListAPIView):
    queryset = News.objects.filter(type=1).order_by('-created_date')[:1]  
    serializer_class = NewsListSerializer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']

    def create(self, validated_data):
        question = validated_data['question']
        if validated_data.get('is_correct', False):
            Answer.objects.filter(question=question).update(is_correct=False)
        return super().create(validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions']



class DiscussionSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'title', 'text', 'image', 'created_date', 'author', 'author_username']
        read_only_fields = ['author', 'created_date']


