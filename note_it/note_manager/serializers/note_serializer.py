from rest_framework import serializers
from ..models import Note
import json

class NoteSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Note
        fields = ('id', 'title', 'content', 'is_pinned','created_at', 'updated_at')

    def get_content(self, obj):
        try:
            data = json.loads(obj.content)
            return data.get('ops', [])
        except json.JSONDecodeError:
            return [] 
        

