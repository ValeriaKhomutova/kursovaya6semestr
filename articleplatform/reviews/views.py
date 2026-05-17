from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import ReviewCreateSerializer
from .models import Review


class ReviewCreate(APIView):

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request):

        article_id = request.data.get("article")

        existing_review = Review.objects.filter(
            author=request.user,
            article_id=article_id
        ).first()

        # ЕСЛИ review уже существует
        if existing_review:

            like = request.data.get(
                "like",
                existing_review.like
            )

            dislike = request.data.get(
                "dislike",
                existing_review.dislike
            )

            # toggle logic

            if existing_review.like and like:
                like = False

            elif existing_review.dislike and dislike:
                dislike = False

            elif like:
                dislike = False

            elif dislike:
                like = False

            existing_review.text = request.data.get(
                "text",
                existing_review.text
            )

            existing_review.like = like
            existing_review.dislike = dislike

            existing_review.save()

            return Response(
                ReviewCreateSerializer(
                    existing_review
                ).data,
                status=status.HTTP_200_OK
            )

        # СОЗДАНИЕ НОВОГО

        serializer = ReviewCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                author=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    
class ReviewDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response(
                {"error": "Review not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 🔒 защита: удалить может только автор
        if review.author != request.user:
            return Response(
                {"error": "You cannot delete this review"},
                status=status.HTTP_403_FORBIDDEN
            )

        review.delete()

        return Response(
            {"message": "Review deleted"},
            status=status.HTTP_204_NO_CONTENT
        )