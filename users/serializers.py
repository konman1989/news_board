from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id",
                  "email",
                  "first_name",
                  "last_name",
                  "password1",
                  "password2"]

    def validate_password2(self, value):
        password1 = self.initial_data.get('password1')

        if password1 != value:
            raise serializers.ValidationError("Passwords don't match!")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user
