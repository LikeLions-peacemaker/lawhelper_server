from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 시리얼라이저"""

    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 'terms_agreed',
            'privacy_agreed', 'marketing_agreed', 'created_at'
        ]
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    """사용자 기본 정보 시리얼라이저"""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """사용자 회원가입 시리얼라이저"""
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    terms_agreed = serializers.BooleanField()
    privacy_agreed = serializers.BooleanField()
    marketing_agreed = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 'last_name',
            'terms_agreed', 'privacy_agreed', 'marketing_agreed'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")

        if not attrs['terms_agreed']:
            raise serializers.ValidationError("이용약관에 동의해야 합니다.")

        if not attrs['privacy_agreed']:
            raise serializers.ValidationError("개인정보처리방침에 동의해야 합니다.")

        return attrs

    def create(self, validated_data):
        # 프로필 관련 데이터 분리
        profile_data = {
            'terms_agreed': validated_data.pop('terms_agreed'),
            'privacy_agreed': validated_data.pop('privacy_agreed'),
            'marketing_agreed': validated_data.pop('marketing_agreed', False),
        }

        # 비밀번호 확인 필드 제거
        validated_data.pop('password_confirm')

        # 사용자 생성 (username을 email로 설정)
        user = User.objects.create_user(
            username=validated_data['email'],
            **validated_data
        )

        # 프로필 업데이트
        for attr, value in profile_data.items():
            setattr(user.profile, attr, value)
        user.profile.save()

        return user


class PasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경 시리얼라이저"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("새 비밀번호가 일치하지 않습니다.")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("기존 비밀번호가 올바르지 않습니다.")
        return value
