from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer, ChoiceSerializer
from .permissions import IsOwnerOrReadOnly


from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


from .permissions import IsAdminOrOwner

class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAdminOrOwner]

class VoteCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, poll_id):
        user = request.user
        choice_id = request.data.get('choice')

        try:
            choice = Choice.objects.get(id=choice_id, poll_id=poll_id)
        except Choice.DoesNotExist:
            return Response({'error': 'Choice not found for this poll'}, status=status.HTTP_404_NOT_FOUND)

        if Vote.objects.filter(user=user, choice__poll_id=poll_id).exists():
            return Response({'error': 'You already voted in this poll'}, status=status.HTTP_400_BAD_REQUEST)

        vote = Vote.objects.create(user=user, choice=choice)
        serializer = VoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChoiceCreateView(generics.CreateAPIView):
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        poll_id = self.kwargs['poll_id']
        poll = Poll.objects.get(id=poll_id)
        serializer.save(poll=poll)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
