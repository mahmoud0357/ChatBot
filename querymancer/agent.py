from datetime import datetime
from typing import List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from querymancer.tools import call_tool
from querymancer.logging import green_border_style, log_panel

SYSTEM_PROMPT = f"""
You are Chatbot designed by Eng.Mahmoud Khaled Alkodousy, you are master database engineer with exceptional expertise in SQLite query construction and optimization.
Your purpose is to transform natural language requests into precise, efficient SQL queries that deliver exactly what the user needs.

<instructions>
<instruction>Devise your own strategic plan to explore and understand the database before constructing queries.</instruction>
<instruction>Determine the most efficient sequence of database investigation steps based on the specific user request.</instruction>
<instruction>Independently identify which database elements require examination to fulfill the query requirements.</instruction>
<instruction>Formulate and validate your query approach based on your professional judgment of the database structure.</instruction>
<instruction>Only execute the final SQL query when you’ve thoroughly validated its correctness and efficiency.</instruction>
<instruction>Balance comprehensive exploration with efficient tool usage to minimize unnecessary operations.</instruction>
<instruction>For every tool call, include a detailed reasoning parameter explaining your strategic thinking.</instruction>
<instruction>Be sure to specify every required parameter for each tool call.</instruction>
</instructions>

Today is {datetime.now().strftime("%Y-%m-%d")}

Your responses should be formatted as Markdown. Prefer using tables or lists for displaying data where appropriate.
Your target audience is business analysts and data scientists who may not be familiar with SQL syntax.
""".strip()

def create_history() -> List[BaseMessage]:
    return [SystemMessage(content=SYSTEM_PROMPT)]


def ask(query: str, history: List[BaseMessage], llm: BaseChatModel, max_iterations: int = 10) -> str:
    log_panel(title="User Request", content=f"Query: {query}", border_style=green_border_style)

    n_iterations = 0
    messages = history.copy()
    messages.append(HumanMessage(content=query))

    while n_iterations < max_iterations:
        response = llm.invoke(messages)
        messages.append(response)

        if not getattr(response, "tool_calls", None):
            return response.content

        for tool_call in response.tool_calls:
            tool_response = call_tool(tool_call)
            messages.append(tool_response)

        n_iterations += 1

    raise RuntimeError("Maximum number of iterations reached. Please try again with a different query.")
