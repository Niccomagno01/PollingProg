# accounts/urls.py
from django.urls import path
from .views import RegisterView, CurrentUserView # Importa CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # Aggiungi questa riga per l'endpoint dell'utente corrente
    path('me/', CurrentUserView.as_view(), name='current_user'),
]
