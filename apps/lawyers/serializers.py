from rest_framework import serializers
from .models import Lawyer, AvailableTime, Review

class AvailableTimeSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = AvailableTime
        fields = ['day_of_week', 'day_name', 'start_time', 'end_time']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['client_name', 'rating', 'comment', 'case_type', 'created_at']

class LawyerListSerializer(serializers.ModelSerializer):
    specialty_display = serializers.CharField(source='get_specialty_display', read_only=True)
    
    class Meta:
        model = Lawyer
        fields = [
            'id', 'name', 'specialty', 'specialty_display', 'experience_years',
            'hourly_rate', 'profile_image', 'rating', 'review_count',
            'consultation_count', 'success_rate'
        ]

class LawyerDetailSerializer(serializers.ModelSerializer):
    specialty_display = serializers.CharField(source='get_specialty_display', read_only=True)
    available_times = AvailableTimeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lawyer
        fields = [
            'id', 'name', 'specialty', 'specialty_display', 'experience_years',
            'description', 'hourly_rate', 'profile_image', 'office_address',
            'phone', 'email', 'rating', 'review_count', 'university',
            'career_highlights', 'consultation_count', 'success_rate',
            'available_times', 'reviews'
        ]