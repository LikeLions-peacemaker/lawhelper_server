from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Lawyer, Review
from .serializers import LawyerListSerializer, LawyerDetailSerializer, ReviewSerializer


class LawyerListView(generics.ListAPIView):

    queryset = Lawyer.objects.all()
    serializer_class = LawyerListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialty']
    search_fields = ['name', 'description', 'university']
    ordering_fields = ['hourly_rate', 'experience_years', 'rating', 'review_count']
    ordering = ['-rating', '-review_count']

class LawyerDetailView(generics.RetrieveAPIView):
    """변호사 상세 정보 API"""
    queryset = Lawyer.objects.all()
    serializer_class = LawyerDetailSerializer

@api_view(['GET'])
def lawyer_search(request):


    """변호사 검색 API"""
    query = request.GET.get('q', '')
    specialty = request.GET.get('specialty', '')
    min_rating = request.GET.get('min_rating', '')
    max_price = request.GET.get('max_price', '')
    
    lawyers = Lawyer.objects.all()
    
    if query:
        lawyers = lawyers.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(university__icontains=query)
        )
    
    if specialty:
        lawyers = lawyers.filter(specialty=specialty)
    
    if min_rating:
        lawyers = lawyers.filter(rating__gte=float(min_rating))
    
    if max_price:
        lawyers = lawyers.filter(hourly_rate__lte=int(max_price))
    
    lawyers = lawyers.order_by('-rating', '-review_count')
    serializer = LawyerListSerializer(lawyers, many=True)
    return Response(serializer.data)

@api_view(['GET'])

def specialty_stats(request):
    """전문분야별 통계"""

    from django.db.models import Count, Avg
    
    stats = Lawyer.objects.values('specialty').annotate(
        count=Count('id'),
        avg_rating=Avg('rating'),
        avg_price=Avg('hourly_rate')
    ).order_by('-count')
    
    for stat in stats:
        stat['specialty_display'] = dict(Lawyer.SPECIALTY_CHOICES)[stat['specialty']]
    
    return Response(stats)