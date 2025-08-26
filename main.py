from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

import os

# --- Load API keys ---
load_dotenv()

# --- Pydantic Schema for structured response ---
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# --- LLM ---
llm = ChatOpenAI(model="gpt-4o-mini")

# --- Parser ---
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# --- Prompt Template ---
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Use tools when necessary.
            Always respond only in this structured format:
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# --- Tools ---
tools = [search_tool, wiki_tool, save_tool]

# --- Agent ---
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Run ---
query = input("What can I help you research? ")
raw_response = agent_executor.invoke({"query": query})

print("\n🔎 Raw Response:", raw_response, "\n")

# --- Parse ---
try:
    # In most LangChain versions, the final answer is under "output"
    structured_response = parser.parse(raw_response["output"])
    print("\n✅ Structured Response:\n", structured_response, "\n")
except Exception as e:
    print("⚠️ Error parsing response:", e)
    print("Raw Response Keys:", raw_response.keys())
    print("Raw Response:", raw_response)
