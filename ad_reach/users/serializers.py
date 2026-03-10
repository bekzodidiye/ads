from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'full_name', 'role', 'balance', 'frozen_balance', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'balance': {'read_only': True},
            'frozen_balance': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
