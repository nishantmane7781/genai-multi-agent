
from flask import Blueprint, request, jsonify
from src.services.genai_service import GenAIService

bp = Blueprint("api", __name__)
svc = GenAIService.instance()

@bp.route("/health")
def health(): return jsonify({"status":"UP"})

@bp.route("/rag/query", methods=["POST"])
def rag():
    q = request.json.get("question")
    return jsonify({"answer": svc.rag_query(q)})

@bp.route("/api/agents/query", methods=["POST"])
def query_agent():
    data = request.json
    question = data.get("question")
    agent = data.get("agent")

    if not question or not agent:
        return jsonify({"error": "question and agent are required"}), 400

    result = svc.query(question, agent)

    return jsonify({
        "agent": agent,
        "answer": result
    })
