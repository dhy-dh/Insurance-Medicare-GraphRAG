#!/usr/bin/env python3
"""
Streamlit UI for Insurance Medicare GraphRAG
"""

import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
API_BASE = f"{BACKEND_URL}/api/v1"


def check_health() -> dict:
    """Check backend health"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.json()
    except Exception as e:
        return {"status": "error", "neo4j": "fail", "llm": "fail", "error": str(e)}


def ask_question(question: str, hop: int = 2, limit: int = 20) -> dict:
    """Ask a question via API"""
    response = requests.post(
        f"{API_BASE}/ask",
        json={"question": question, "hop": hop, "limit": limit},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main():
    st.set_page_config(
        page_title="保险知识图谱问答系统",
        page_icon="🏥",
        layout="wide",
    )

    st.title("🏥 保险知识图谱问答系统")
    st.markdown("基于知识图谱的保险产品咨询助手")

    # Sidebar - Status
    with st.sidebar:
        st.header("系统状态")

        # Health check
        health = check_health()

        if health.get("status") == "ok":
            st.success("✅ 系统正常")
        else:
            st.error("❌ 系统异常")

        st.write(f"**Neo4j**: {'✅' if health.get('neo4j') == 'ok' else '❌'}")
        st.write(f"**LLM**: {'✅' if health.get('llm') == 'ok' else '❌'}")

        st.divider()

        # Settings
        st.header("参数设置")

        hop = st.slider("图谱检索跳数", min_value=1, max_value=3, value=2)
        limit = st.slider("证据数量限制", min_value=5, max_value=50, value=20)

    # Main content
    st.subheader("请输入您的问题")

    # Question input
    question = st.text_input(
        "问题",
        placeholder="例如：70岁高血压能买XX护理险吗？",
        label_visibility="collapsed",
    )

    # Example questions
    st.markdown("**示例问题：**")
    examples = [
        "70岁高血压能买XX护理险吗？",
        "60岁老人可以购买哪些护理险？",
        "糖尿病患者是否被XX医疗险承保？",
    ]
    cols = st.columns(len(examples))
    for i, ex in enumerate(examples):
        if cols[i].button(ex, key=f"ex_{i}"):
            question = ex
            st.rerun()

    # Submit button
    if st.button("提交问题", type="primary", disabled=not question):
        with st.spinner("正在查询知识图谱..."):
            try:
                result = ask_question(question, hop=hop, limit=limit)

                # Display answer
                st.divider()
                st.subheader("📝 回答")

                # Confidence badge
                confidence = result.get("confidence", "low")
                if confidence == "high":
                    st.success(f"置信度: {confidence.upper()}")
                elif confidence == "medium":
                    st.warning(f"置信度: {confidence.upper()}")
                else:
                    st.info(f"置信度: {confidence.upper()}")

                st.markdown(f"### {result.get('answer', '')}")

                # Citations
                st.subheader("📚 引用证据")
                citations = result.get("citations", [])
                if citations:
                    for i, cite in enumerate(citations, 1):
                        with st.expander(f"证据 {i}"):
                            st.code(cite.get("triple", ""))
                            if cite.get("source_id"):
                                st.caption(f"来源: {cite['source_id']}")
                else:
                    st.info("暂无引用证据")

                # Debug info (collapsible)
                with st.expander("🔧 调试信息"):
                    debug = result.get("debug", {})

                    st.write("**识别的实体:**")
                    entities = debug.get("linked_entities", [])
                    if entities:
                        for e in entities:
                            st.write(f"- {e.get('mention')} → {e.get('node_id')} ({e.get('label')}, 得分: {e.get('score', 0):.2f})")
                    else:
                        st.write("无")

                    st.write(f"**使用的证据数量:** {debug.get('triples_used', 0)}")

                    st.write("**Cypher查询:**")
                    st.code(debug.get("cypher", ""))

            except requests.exceptions.RequestException as e:
                st.error(f"请求失败: {str(e)}")
            except Exception as e:
                st.error(f"发生错误: {str(e)}")

    # History
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display history (optional)
    # st.divider()
    # st.subheader("历史记录")
    # for item in st.session_state.history[-5:]:
    #     st.write(f"- {item}")


if __name__ == "__main__":
    main()
