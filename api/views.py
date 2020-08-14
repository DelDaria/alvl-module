from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues import models as iss_models
from issues.models import Comment
from .serializers1 import IssueSerializer, CommentSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    # queryset = iss_models.Issue.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            priority = self.request.query_params.get('priority', None)
            if priority is not None:
                return iss_models.Issue.objects.filter(priority=priority)
            return iss_models.Issue.objects.all()
        else:
            return iss_models.Issue.objects.filter(author=self.request.user.id)

    @action(detail=True, methods=['get', 'post'])
    def get_comments(self, request, pk=None):
        queryset = Comment.objects.filter(issue=pk)
        comment = CommentSerializer(queryset, many=True)
        data = comment.data
        return Response(data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # queryset = iss_models.Comment.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return iss_models.Comment.objects.all()
        else:
            return iss_models.Comment.objects.filter(author=self.request.user.id)

