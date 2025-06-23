# from rest_framework import serializers
# from temuapp.models import ChatSession, ChatMessage

# class ChatMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatMessage
#         fields = ['id', 'sender', 'message', 'created_at']

# class ChatSessionSerializer(serializers.ModelSerializer):
#     messages = ChatMessageSerializer(many=True, read_only=True)

#     class Meta:
#         model = ChatSession
#         fields = ['id', 'user', 'created_at', 'messages']