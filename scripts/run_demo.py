#!/usr/bin/env python3
"""
Run demo questions against the GraphRAG API

Usage:
    python run_demo.py --backend-url http://localhost:8000
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime


def load_questions(questions_file: str) -> list:
    """Load evaluation questions"""
    with open(questions_file, "r", encoding="utf-8") as f:
        return json.load(f)


def ask_question(backend_url: str, question: str, hop: int = 2, limit: int = 20) -> dict:
    """Ask a question via API"""
    response = requests.post(
        f"{backend_url}/api/v1/ask",
        json={"question": question, "hop": hop, "limit": limit},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def save_result(result_file: str, results: list):
    """Save results to JSONL"""
    with open(result_file, "a", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Run demo questions")
    parser.add_argument(
        "--backend-url",
        default=os.environ.get("BACKEND_URL", "http://localhost:8000"),
        help="Backend URL",
    )
    parser.add_argument(
        "--questions-file",
        default="docs/eval_questions.json",
        help="Questions file",
    )
    parser.add_argument(
        "--output-file",
        default="data/logs/demo_results.jsonl",
        help="Output file for results",
    )
    parser.add_argument(
        "--hop",
        type=int,
        default=2,
        help="Hop count for subgraph",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Evidence limit",
    )
    args = parser.parse_args()

    # Check backend health
    print(f"Checking backend at {args.backend_url}...")
    try:
        response = requests.get(f"{args.backend_url}/health", timeout=5)
        health = response.json()
        print(f"Health: {health}")
        if health.get("status") != "ok":
            print("❌ Backend is not healthy")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        sys.exit(1)

    # Load questions
    print(f"Loading questions from {args.questions_file}...")
    questions = load_questions(args.questions_file)
    print(f"Found {len(questions)} questions")

    # Create output directory
    output_dir = os.path.dirname(args.output_file)
    os.makedirs(output_dir, exist_ok=True)

    # Run questions
    results = []
    success_count = 0
    error_count = 0

    print("\nRunning questions...")
    for i, q in enumerate(questions, 1):
        question_text = q.get("question", "")
        print(f"\n[{i}/{len(questions)}] {question_text}")

        try:
            start_time = time.time()
            result = ask_question(
                args.backend_url,
                question_text,
                hop=args.hop,
                limit=args.limit,
            )
            elapsed = time.time() - start_time

            results.append({
                "timestamp": datetime.now().isoformat(),
                "question_id": q.get("id"),
                "question": question_text,
                "category": q.get("category"),
                "answer": result.get("answer"),
                "confidence": result.get("confidence"),
                "citations_count": len(result.get("citations", [])),
                "elapsed_seconds": round(elapsed, 2),
                "status": "success",
            })

            print(f"  ✅ Confidence: {result.get('confidence')}, Citations: {len(result.get('citations', []))}, Time: {elapsed:.2f}s")
            success_count += 1

        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                "timestamp": datetime.now().isoformat(),
                "question_id": q.get("id"),
                "question": question_text,
                "category": q.get("category"),
                "status": "error",
                "error": str(e),
            })
            error_count += 1

    # Save results
    save_result(args.output_file, results)

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total questions: {len(questions)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Results saved to: {args.output_file}")


if __name__ == "__main__":
    main()
