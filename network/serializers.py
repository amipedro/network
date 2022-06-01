from rest_framework import serializers
from network.models import Woof
from network.models import User
# from network.models import Following


class WoofSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = Woof
        fields = ('id', 'username', 'first_name', 'last_name', 'text', 'created_at',
                  'updated_at', 'likes')
        # read_only_fields = ('id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'following', 'followers', 'date_joined')
        extra_kwargs = {"followers": {"required": False, "allow_null": True}}


# class FollowingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Following
#         fields = ('id', 'user', 'following')


# class FollowCountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'followers_count', 'following_count')
