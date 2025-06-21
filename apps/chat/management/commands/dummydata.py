# management/commands/create_dummy_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time
import random
from faker import Faker
from apps.lawyers.models import Lawyer, AvailableTime, Review

fake = Faker('ko_KR')

class Command(BaseCommand):
    help = '변호사 더미 데이터 생성'

    def handle(self, *args, **options):
        # 기존 데이터 삭제
        Lawyer.objects.all().delete()
        AvailableTime.objects.all().delete()
        Review.objects.all().delete()

        lawyers_data = [
            {
                'name': '김민수',
                'specialty': 'civil',
                'experience_years': 15,
                'description': '15년간 민사소송 전문으로 활동하고 있습니다. 부동산, 손해배상, 계약분쟁 등 다양한 민사 사건을 담당해왔습니다.',
                'hourly_rate': 300000,
                'office_address': '서울시 강남구 테헤란로 123',
                'phone': '02-1234-5678',
                'email': 'kim.minsu@law.com',
                'rating': 4.8,
                'review_count': 127,
                'university': '서울대학교 법학과',
                'career_highlights': '대한변호사협회 우수변호사상 수상, 민사소송 승률 92%',
                'consultation_count': 450,
                'success_rate': 92
            },
            {
                'name': '박지영',
                'specialty': 'family',
                'experience_years': 12,
                'description': '가족법 전문 변호사로서 이혼, 양육권, 상속 등의 사건을 주로 담당합니다. 의뢰인의 마음을 이해하는 상담을 제공합니다.',
                'hourly_rate': 250000,
                'office_address': '서울시 서초구 서초중앙로 45',
                'phone': '02-2345-6789',
                'email': 'park.jiyoung@law.com',
                'rating': 4.9,
                'review_count': 89,
                'university': '연세대학교 법학과',
                'career_highlights': '가족법 전문변호사, 이혼전문상담사 자격',
                'consultation_count': 320,
                'success_rate': 88
            },
            {
                'name': '이철호',
                'specialty': 'criminal',
                'experience_years': 20,
                'description': '형사법 전문으로 20년간 활동해온 베테랑 변호사입니다. 무죄 판결 경험이 풍부하며, 치밀한 변론으로 유명합니다.',
                'hourly_rate': 400000,
                'office_address': '서울시 중구 을지로 78',
                'phone': '02-3456-7890',
                'email': 'lee.cheolho@law.com',
                'rating': 4.7,
                'review_count': 156,
                'university': '고려대학교 법학과',
                'career_highlights': '형사전문변호사, 검찰청 출신',
                'consultation_count': 680,
                'success_rate': 85
            },
            {
                'name': '정수연',
                'specialty': 'corporate',
                'experience_years': 8,
                'description': '기업법무 전문 변호사로서 계약검토, 컴플라이언스, M&A 등을 담당합니다. 스타트업부터 대기업까지 다양한 경험이 있습니다.',
                'hourly_rate': 350000,
                'office_address': '서울시 강남구 역삼로 234',
                'phone': '02-4567-8901',
                'email': 'jung.suyeon@law.com',
                'rating': 4.6,
                'review_count': 73,
                'university': '성균관대학교 법학과',
                'career_highlights': '기업법무 전문, 로펌 파트너 출신',
                'consultation_count': 280,
                'success_rate': 90
            },
            {
                'name': '최영진',
                'specialty': 'labor',
                'experience_years': 18,
                'description': '노동법 전문 변호사로서 부당해고, 임금체불, 산업재해 등의 사건을 담당합니다. 근로자의 권익 보호에 앞장서고 있습니다.',
                'hourly_rate': 280000,
                'office_address': '서울시 영등포구 여의도동 567',
                'phone': '02-5678-9012',
                'email': 'choi.youngjin@law.com',
                'rating': 4.8,
                'review_count': 134,
                'university': '이화여자대학교 법학과',
                'career_highlights': '노동부 자문변호사, 노동법 전문변호사',
                'consultation_count': 520,
                'success_rate': 87
            }
        ]

        for lawyer_data in lawyers_data:
            lawyer = Lawyer.objects.create(**lawyer_data)
            
            # 상담 가능 시간 추가 (월-금 9시-18시)
            for day in range(5):  # 월-금
                AvailableTime.objects.create(
                    lawyer=lawyer,
                    day_of_week=day,
                    start_time=time(9, 0),
                    end_time=time(18, 0)
                )
            
            # 리뷰 데이터 추가
            review_templates = [
                {'comment': '정말 친절하고 자세한 상담을 해주셨습니다. 덕분에 좋은 결과를 얻을 수 있었어요.', 'case_type': '계약분쟁'},
                {'comment': '전문적인 조언과 함께 마음의 위로도 받을 수 있었습니다. 추천합니다!', 'case_type': '이혼소송'},
                {'comment': '치밀한 준비와 탁월한 변론 실력으로 승소할 수 있었습니다.', 'case_type': '민사소송'},
                {'comment': '어려운 상황에서도 끝까지 최선을 다해주셨어요. 감사합니다.', 'case_type': '형사사건'},
                {'comment': '상담비가 조금 비싸긴 하지만 그만한 가치가 있다고 생각합니다.', 'case_type': '기업법무'},
            ]
            
            # 리뷰 생성
            review_count = min(lawyer.review_count, 10)  # 최대 10개까지만
            for i in range(review_count):
                review_data = random.choice(review_templates)
                Review.objects.create(
                    lawyer=lawyer,
                    client_name=fake.name(),
                    rating=random.choice([4, 5]) if lawyer.rating >= 4.5 else random.choice([3, 4, 5]),
                    comment=review_data['comment'],
                    case_type=review_data['case_type']
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(lawyers_data)} lawyers with dummy data')
        )