from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class LogoutView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response(status=400)


class PrivateChatCreateView(generics.CreateAPIView):
    serializer_class = PrivateChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user2_id = request.data.get('user2_id')
        user2 = CustomUser.objects.get(id=user2_id)

        chat, created = PrivateChat.objects.get_or_create(
            user1=min(request.user, user2, key=lambda u: u.id),
            user2=max(request.user, user2, key=lambda u: u.id)
        )

        serializer = self.get_serializer(chat)
        return Response(serializer.data)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = PrivateChat.objects.get(id=chat_id)
        serializer.save(sender=self.request.user, chat=chat)
