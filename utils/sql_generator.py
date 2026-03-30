import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


load_dotenv()
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    max_new_tokens=2048,
)
client = ChatHuggingFace(llm=llm)

def generate_sql_from_question(question, schema):

    prompt = f"""
You are an expert SQL data analyst.

Generate a SQL query for the user's question.

Database schema:
{schema}

Rules:
- Only generate SELECT queries
- Use correct table and column names
- Use aggregation when needed

User question:
{question}

Return only SQL.
"""

    response = client.invoke([HumanMessage(content=prompt)])
    sql = response.content.strip()

    return sql
