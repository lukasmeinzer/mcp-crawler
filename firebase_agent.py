from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv(override=True)


async def run_agent(user_input):

    mcp_server_params = StdioServerParameters(
        command="npx",
        env={"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
        args=["firecrawl-mcp"]
    )

    brain_model = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    async with stdio_client(mcp_server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(brain_model, tools)
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can scrape websites using Firecrawl. Think step by step."
                },
                {"role": "user", "content": user_input[:175000]}
            ]
            result = await agent.ainvoke({"messages": messages}, maxDepth=10)
            return result["messages"][-1].content
