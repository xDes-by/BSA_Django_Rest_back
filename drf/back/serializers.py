from rest_framework import serializers

from .models import User, UserProfile, UserItems


class UserItemsSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', max_length=200)
    can_upgrade = serializers.CharField(source='product.can_upgrade', max_length=200)

    class Meta:
        model = UserItems
        fields = ['count', 'active', 'product', 'can_upgrade']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    product = UserItemsSerializer(many=True, read_only=True)
    profile = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['steamID', 'product', 'profile', 'coins', 'rp', 'total_coins', 'ban_status']
