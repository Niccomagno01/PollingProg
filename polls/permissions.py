
# polls/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permetti richieste di lettura a tutti
        if request.method in SAFE_METHODS:
            return True
        # Permetti solo al creatore dell'oggetto di modificarlo/eliminarlo
        # Assicurati che l'utente sia autenticato e che sia il creatore
        return obj.created_by == request.user

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # I superuser possono fare qualsiasi cosa
        if request.user and request.user.is_staff:
            return True
        # I metodi sicuri (GET, HEAD, OPTIONS) sono permessi a tutti
        if request.method in SAFE_METHODS:
            return True
        # Permetti al creatore del sondaggio di modificarlo/eliminarlo
        return obj.created_by == request.user