from rest_framework.views import APIView, Response, status
from .serializer import Books, UserBook
from library_app.models import Book
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView

class BookViewPagination(PageNumberPagination):
    page_size = 2

class BookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = Books
    pagination_class = BookViewPagination



#    def get(self, request):
#        serializer = Books(instance=Book.objects.all(), many=True, context={'request': request})
#        return Response(data=serializer.data, status=status.HTTP_200_OK)
#    
#    def post(self, request):
#        serializer = Books(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        return Response(data=serializer.data)
       

       


class UserView(APIView):

    def get(self, request, pk):
        serializer = UserBook(instance=User.objects.get(pk=pk), many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)