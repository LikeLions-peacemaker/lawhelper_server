from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Lawyer(models.Model):
    SPECIALTY_CHOICES = [
        ('civil', '민사법'),
        ('criminal', '형사법'),
        ('family', '가족법'),
        ('corporate', '기업법'),
        ('tax', '세무법'),
        ('labor', '노동법'),
        ('real_estate', '부동산법'),
        ('intellectual_property', '지적재산권법'),
        ('medical', '의료법'),
        ('environmental', '환경법'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='이름')
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, verbose_name='전문분야')
    experience_years = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='경력년수')
    description = models.TextField(verbose_name='소개')
    hourly_rate = models.IntegerField(verbose_name='시간당 상담료')
    profile_image = models.URLField(blank=True, verbose_name='프로필 이미지')
    office_address = models.CharField(max_length=200, verbose_name='사무실 주소')
    phone = models.CharField(max_length=15, verbose_name='전화번호')
    email = models.EmailField(verbose_name='이메일')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0, verbose_name='평점')
    review_count = models.IntegerField(default=0, verbose_name='리뷰 수')
    university = models.CharField(max_length=100, verbose_name='출신대학')
    career_highlights = models.TextField(blank=True, verbose_name='주요 경력')
    consultation_count = models.IntegerField(default=0, verbose_name='상담 건수')
    success_rate = models.IntegerField(default=85, verbose_name='승률')
    
    class Meta:
        verbose_name = '변호사'
        verbose_name_plural = '변호사들'
    
    def __str__(self):
        return f"{self.name} - {self.get_specialty_display()}"

class AvailableTime(models.Model):
    WEEKDAY_CHOICES = [
        (0, '월요일'),
        (1, '화요일'),
        (2, '수요일'),
        (3, '목요일'),
        (4, '금요일'),
        (5, '토요일'),
        (6, '일요일'),
    ]
    
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='available_times')
    day_of_week = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        verbose_name = '상담 가능 시간'
        verbose_name_plural = '상담 가능 시간들'

class Review(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, related_name='reviews')
    client_name = models.CharField(max_length=50, verbose_name='의뢰인')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='평점')
    comment = models.TextField(verbose_name='리뷰 내용')
    case_type = models.CharField(max_length=50, verbose_name='사건 유형')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    
    class Meta:
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰들'
        ordering = ['-created_at']