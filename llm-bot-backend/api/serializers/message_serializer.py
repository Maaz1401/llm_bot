from rest_framework import serializers
from api.models import Message, User
from .document_serializer import DocumentSerializer


class MessageSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)
    document_id = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all(), write_only=True, required=False)
    user_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'session',
            'message_type',
            'document',
            'document_id',
            'user',
            'user_data',
            'created_at'
        )
        read_only_fields = ('document', 'user_data',)

    def get_user_data(self, obj):
        if not obj.user:
            return None
        user = User.objects.get(pk=obj.user.id)
        data = {
            'username': user.username,
            'role_code': user.role.code_name,
        }
        return data