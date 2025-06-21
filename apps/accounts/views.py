from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    PasswordChangeSerializer, UserProfileSerializer
)
from .models import UserProfile


class UserRegistrationView(generics.CreateAPIView):
    """사용자 회원가입 API"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': '회원가입이 완료되었습니다. AI 법률 상담을 시작해보세요!'
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """사용자 프로필 조회/수정 API"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """비밀번호 변경 API"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def custom_login(request):
    """커스텀 로그인 API"""
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'error': '이메일과 비밀번호를 입력해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': f'환영합니다, {user.profile.full_name}님!'
        })
    else:
        return Response({
            'error': '이메일 또는 비밀번호가 올바르지 않습니다.'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info(request):
    """현재 로그인한 사용자 정보 조회"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """API 서버 상태 확인"""
    return Response({
        'status': 'healthy',
        'message': 'LawHelper Server is running',
        'version': '1.0.0'
    })
