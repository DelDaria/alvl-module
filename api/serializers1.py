from rest_framework import serializers
from issues import models as iss_models
from issues import models as iss_models
from users import models as us_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = us_models.User
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = iss_models.Issue
        # fields = '__all__'
        exclude = ('i',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = iss_models.Comment
        fields = '__all__'
