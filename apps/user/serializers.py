from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    role_display_uz = serializers.CharField(source='get_role_display_uz', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    is_operator = serializers.BooleanField(read_only=True)
    is_supervisor = serializers.BooleanField(read_only=True)
    is_specialist = serializers.BooleanField(read_only=True)
    role_level = serializers.IntegerField(source='get_role_level', read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "role",
            "role_display",
            "role_display_uz",
            "employee_id",
            "is_active",
            "shift",
            "is_operator",
            "is_supervisor", 
            "is_specialist",
            "role_level",
            "profile_picture",
            "created_at",
            "updated_at",
        ]


