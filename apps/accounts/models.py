# apps/accounts/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """사용자 프로필 모델"""

    # 기본 정보
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')

    # 프로필 이미지
    profile_image = models.ImageField(
        upload_to='profiles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='프로필 이미지'
    )

    # 소셜 로그인 정보
    is_social_account = models.BooleanField(
        default=False, verbose_name='소셜 계정 여부')
    social_provider = models.CharField(
        max_length=20, blank=True, verbose_name='소셜 제공자')

    # 약관 동의
    terms_agreed = models.BooleanField(default=False, verbose_name='이용약관 동의')
    privacy_agreed = models.BooleanField(
        default=False, verbose_name='개인정보처리방침 동의')
    marketing_agreed = models.BooleanField(
        default=False, verbose_name='마케팅 수신 동의')

    # 메타 정보
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    is_active = models.BooleanField(default=True, verbose_name='활성 상태')

    class Meta:
        verbose_name = '사용자 프로필'
        verbose_name_plural = '사용자 프로필들'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}"

    @property
    def full_name(self):
        """전체 이름 반환"""
        return f"{self.user.last_name}{self.user.first_name}"


# 시그널을 사용한 자동 프로필 생성
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """사용자 생성 시 자동으로 프로필 생성"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """사용자 저장 시 프로필도 함께 저장"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
