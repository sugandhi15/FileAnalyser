from rest_framework import serializers
from .models import Document, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['user', 'file', 'uploaded_at']
        # extra_kwargs = {
        #     'user': {'required': True},
        # }