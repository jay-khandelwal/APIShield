from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['user_id']
        return super().create(validated_data)
