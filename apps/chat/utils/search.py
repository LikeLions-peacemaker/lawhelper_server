import pandas as pd
import numpy as np
import json
from apps.chat.models import Embedding
from openai import OpenAI
from typing import List
from scipy import spatial
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

def load_embeddings_df():
    # DB에서 임베딩 전체 조회 (n_tokens 필드가 모델에 없으면 아래에서 계산)
    qs = Embedding.objects.all().values('text', 'embedding')
    rows = []
    for obj in qs:
        text = obj['text']
        embedding = json.loads(obj['embedding'])  # 문자열 → 리스트
        n_tokens = len(text)  # 필요시 tiktoken으로 교체
        rows.append({'text': text, 'embeddings': embedding, 'n_tokens': n_tokens})
    return pd.DataFrame(rows)

def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[float]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances

def create_context(question, df, max_len=1800):
    """질문과 학습 데이터를 비교해 컨텍스트를 만드는 함수"""

    # 질문을 벡터화
    q_embeddings = client.embeddings.create(
        input=[question], model='text-embedding-3-small'
    ).data[0].embedding

    # 코사인 유사도 계산
    df['distances'] = distances_from_embeddings(
        q_embeddings,
        df['embeddings'].values,  # 이미 np.array(embedding) 형태임
        distance_metric='cosine'
    )

    returns = []
    cur_len = 0

    # 유사도 순으로 정렬, 토큰 개수 한도 내에서 텍스트 추가
    for _, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])

    return "\n\n###\n\n".join(returns)

def answer_question(question, conversation_history):
    """문맥에 따라 질문에 JSON으로 정답하는 기능"""

    df = load_embeddings_df()
    context = create_context(question, df, max_len=200)

    system_prompt = """
당신은 전문적인 법률 자문을 제공하는 AI 챗봇 'Law Helper'입니다.

사용자의 질문을 분석하여 반드시 아래 형식의 JSON으로만 응답하세요.

예시 형식:
{
    "response": "답변 내용",
    "references": ["참고 자료 또는 법률 조항"]
}

답변은 간결하고 명확하며, 법률 용어를 정확히 사용해야 합니다.
""".strip()

    # 1. system 프롬프트 먼저 삽입
    messages = [{"role": "system", "content": system_prompt}]

    # 2. 이전 대화가 있다면 추가
    for turn in conversation_history:
        if turn.get("role") in ["user", "assistant"]:
            messages.append({"role": turn["role"], "content": turn["content"]})

    # 3. 마지막 질문을 현재 문맥 포함해서 user로 추가
    prompt = f"""
문맥:
{context}

---

질문: {question}
답변:
""".strip()

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            temperature=0.3,
        )
        answer = response.choices[0].message.content.strip()
        
        # 대화 기록 업데이트 (optional)
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "assistant", "content": answer})

        return answer
    except Exception as e:
        print(e)
        return ""
