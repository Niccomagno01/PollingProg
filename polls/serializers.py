from rest_framework import serializers
from .models import Poll, Choice, Vote
from django.contrib.auth import get_user_model

User = get_user_model()

class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes_count']
        read_only_fields = ['votes_count']

    def get_votes_count(self, obj):
        return obj.votes.count()

class PollSerializer(serializers.ModelSerializer):

    choices = ChoiceSerializer(many=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'choices', 'created_at']
        read_only_fields = ['created_at'] # La data di creazione è in sola lettura

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        poll = Poll.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(poll=poll, **choice_data)
        return poll

    def update(self, instance, validated_data):

        instance.question = validated_data.get('question', instance.question)
        instance.save()


        choices_data = validated_data.pop('choices', [])
        instance.choices.all().delete() # Cancella tutte le scelte esistenti

        for choice_data in choices_data:
            Choice.objects.create(poll=instance, **choice_data)

        return instance

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Vote
        fields = ['id', 'user', 'choice']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'email']