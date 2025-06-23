# gptbot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils.search import answer_question
from django.shortcuts import render
from .models import ChatMessage, ChatSession
conversation_history = [{"role": "system", "content": "hi"}]
@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode())
            session_id = body.get("session_id")
            user_input = body.get("user_input")

            if not user_input or not session_id:
                return JsonResponse({"error": "입력이 부족합니다."}, status=400)

            # 세션 없으면 생성
            session_obj, _ = ChatSession.objects.get_or_create(session_id=session_id)

            # 유저 질문 저장
            ChatMessage.objects.create(
                session=session_obj,
                sender="user",
                message=user_input
            )

            # 대화 히스토리 불러오기
            prev_messages = session_obj.messages.order_by("timestamp")
            conversation_history = [{"role": m.sender, "content": m.message} for m in prev_messages]

            # GPT 응답 생성
            full_answer = answer_question(user_input, conversation_history)

            # GPT 응답 저장
            ChatMessage.objects.create(
                session=session_obj,
                sender="bot",
                message=full_answer
            )

            # response 부분만 파싱
            if isinstance(full_answer, str):
                try:
                    parsed = json.loads(full_answer)
                    only_response = parsed.get("response", "no response")
                except json.JSONDecodeError:
                    only_response = "응답 형식이 올바르지 않습니다."
            else:
                only_response = "응답이 문자열 형식이 아닙니다."

            return JsonResponse({"answer": only_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST method required"}, status=405)

  
  
  

@csrf_exempt
def list_sessions(request):
    if request.method == "GET":
        sessions = ChatSession.objects.all().order_by('-created_at')
        data = [{"session_id": s.session_id, "title": s.title} for s in sessions]
        return JsonResponse({"sessions": data})
@csrf_exempt
def load_history(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode())
            session_id = body.get("session_id")
            if not session_id:
                return JsonResponse({"error": "세션 ID 필요"}, status=400)

            messages = ChatMessage.objects.filter(session_id=session_id).order_by("timestamp")
            data = [{"sender": m.sender, "message": m.message} for m in messages]
            return JsonResponse({"history": data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "POST만 허용"}, status=405)


@csrf_exempt
def chat_page(request):
    return render(request, "chat.html")