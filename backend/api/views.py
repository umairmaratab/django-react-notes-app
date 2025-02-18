from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note

# Creating Note view
class NoteListCreate(generics.ListCreateAPIView): # List view will list notes user created or create new note
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated] # To call this route you should be authenticated (JWT)

    # Get current user notes
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid(): # if note data is valid
            serializer.save(author=self.request.user) # Add field manual as we set it manually
        else:
            print(serializer.errors)

# Deleting Note view
class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    # Get current user notes
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() # Check if user already exists.
    serializer_class = UserSerializer # user model
    permission_classes = [AllowAny] # Anyone can register
