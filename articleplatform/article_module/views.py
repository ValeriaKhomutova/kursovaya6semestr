from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Article
from .serializers import ArticleSerializer

class ArticleCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ArticleList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        articles = Article.objects.all().order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MyArticleList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        articles = Article.objects.filter(author=request.user).order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)