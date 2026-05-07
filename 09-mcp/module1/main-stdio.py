from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport, StdioTransport
from lomond import response
from mcp import stdio_client
import asyncio

stdio_transport = StdioTransport(
    command = "npx",
    args=["-y", "@upstash/context7-mcp"]
)
#print(stdio_transport )

stdio_client = Client(stdio_transport)
async def main():
    async with stdio_client as client:
        # List of tools the server provides
        tools = await client.list_tools()

    print(tools[0].name)

async def mainTools():
    async with stdio_client as client:
        # Find a library ID via a search query
        response = await client.call_tool("resolve-library-id", {
            "libraryName": "fastmcp",
            "query": "I want to create a new MCP server using the fastmcp Python framework"
        })

    print(response.content[0].text)

async def mainToolsLib():
    async with stdio_client as client:
        # Use resolved ID to fetch documentation
        docs = await client.call_tool("query-docs", {
            "libraryId": "/llmstxt/gofastmcp_llms-full_txt",
            "query": "I want to fetch the code snippets and the documentation",
            "tokens": 5000
        })

    print(docs.content[0].text[:1000])


asyncio.run(mainToolsLib())