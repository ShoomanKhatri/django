from rest_framework import generics
from .models import Todo
from .serializers import TodoSerializer

# GET all + POST create
class TodoListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    
# GET single + PUT + DELETE
class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

