# accounts/views.py
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated # Importa IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer # Importa anche UserSerializer
from .models import CustomUser # Importa il tuo CustomUser model

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# NUOVA VISTA: Per ottenere i dettagli dell'utente corrente
class CurrentUserView(generics.RetrieveAPIView):
    """
    Vista per recuperare i dettagli dell'utente autenticato.
    Richiede autenticazione.
    """
    serializer_class = UserSerializer # Usa il UserSerializer che include id e is_staff
    permission_classes = [IsAuthenticated] # Solo gli utenti autenticati possono accedere a questa vista

    def get_object(self):
        """
        Restituisce l'oggetto utente associato alla richiesta corrente.
        """
        return self.request.user
