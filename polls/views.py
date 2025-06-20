from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer
from .permissions import IsOwnerOrReadOnly


class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]


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

# Create your views here.
