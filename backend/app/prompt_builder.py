from typing import List
from app.models import Triple

SYSTEM_PROMPT = """你是一个保险咨询专家。你的职责是根据提供的证据（三元组）回答用户的问题。

重要规则：
1. 只根据提供的三元组证据进行回答，禁止编造信息
2. 如果证据不足以回答问题，明确说明"无法判断"，并列出需要补充的信息
3. 回答必须包含对证据的引用（使用source_id）
4. 用中文回答

回答格式：
- 结论：根据证据说明答案
- 依据：列出引用的证据（source_id）
- 需要补充：如证据不足，说明还需要什么信息
"""


def build_prompt(question: str, triples: List[Triple]) -> str:
    """Build prompt for LLM"""

    # Format triples
    triples_text = ""
    for i, t in enumerate(triples, 1):
        source_info = f" [source_id={t.source_id}]" if t.source_id else ""
        triples_text += f"{i}) ({t.h}, {t.r}, {t.t}){source_info}\n"

    user_prompt = f"""用户问题：{question}

证据三元组：
{triples_text if triples_text else "（无证据）"}

请根据上述证据回答问题。"""

    return f"{SYSTEM_PROMPT}\n\n{user_prompt}"
