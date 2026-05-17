from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import ReviewCreateSerializer
from .models import Review


class ReviewCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(
                ReviewCreateSerializer(serializer.instance).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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