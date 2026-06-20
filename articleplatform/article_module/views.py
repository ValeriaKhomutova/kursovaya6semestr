from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Article
from .serializers import ArticleSerializer
from users.permissions import IsAdminOrAuthor

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
        queryset = Article.objects.all().order_by('-created_at')

        search = request.query_params.get('search')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(subtitle__icontains=search) |
                Q(keywords__icontains=search) |
                Q(specialization__icontains=search)
            )

        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MyArticleList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.role == "admin":
            articles = Article.objects.all().order_by('-created_at')
        else:
            articles = Article.objects.filter(
                author=request.user
            ).order_by('-created_at')

        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ArticleUpdate(APIView):
    permission_classes = [IsAdminOrAuthor]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def put(self, request, pk):
        article = self.get_object(pk)
        self.check_object_permissions(request, article)

        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        article = self.get_object(pk)
        self.check_object_permissions(request, article)

        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ArticleDelete(APIView):
    permission_classes = [IsAdminOrAuthor]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def delete(self, request, pk):
        article = self.get_object(pk)
        self.check_object_permissions(request, article)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)