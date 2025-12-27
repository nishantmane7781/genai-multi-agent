from src.agents.agent_domains import AGENT_DOMAINS

def is_question_in_domain(question: str, agent: str) -> bool:
    question = question.lower()
    keywords = AGENT_DOMAINS.get(agent, [])
    return any(keyword in question for keyword in keywords)
