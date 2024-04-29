from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import Session, Message

class LastConversationView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk=None, format=None):
        sessions = Session.objects.filter(user=request.user)
        if sessions:
            session = sessions.last()
            messages = list(session.messages.all().values('role','content', 'message_type','document'))
        else:
            session = None
            messages = []

        response_data = {
            'session': session.id if session else None,
            'messages': messages
        }

        return Response(status=status.HTTP_200_OK, data=response_data)
