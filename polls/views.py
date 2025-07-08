# polls/views.py
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer, ChoiceSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    # Applica la nuova permission IsAdminOrOwner
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

        # Controlla se l'utente ha già votato in questo sondaggio
        if Vote.objects.filter(user=user, choice__poll_id=poll_id).exists():
            return Response({'error': 'You already voted in this poll'}, status=status.HTTP_400_BAD_REQUEST)

        vote = Vote.objects.create(user=user, choice=choice)
        serializer = VoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Puoi mantenere ChoiceCreateView se vuoi un endpoint separato per aggiungere scelte.
# Tuttavia, il PollSerializer ora supporta la creazione/aggiornamento delle scelte
# insieme al sondaggio principale.
class ChoiceCreateView(generics.CreateAPIView):
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        poll_id = self.kwargs['poll_id']
        poll = Poll.objects.get(id=poll_id)
        # Assicurati che solo il creatore del sondaggio o un superuser possa aggiungere scelte
        if self.request.user != poll.created_by and not self.request.user.is_staff:
            return Response({'error': 'You do not have permission to add choices to this poll.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(poll=poll)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)