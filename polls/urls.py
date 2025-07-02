from django.urls import path
from .views import PollListCreateView, PollDetailView, VoteCreateView, ChoiceCreateView, CurrentUserView

urlpatterns = [
    path('polls/', PollListCreateView.as_view(), name='poll-list'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/<int:poll_id>/vote/', VoteCreateView.as_view(), name='poll-vote'),
    path('polls/<int:poll_id>/choices/', ChoiceCreateView.as_view(), name='choice-create'),
    path('api/user/me/', CurrentUserView.as_view(), name='current-user'),
]

