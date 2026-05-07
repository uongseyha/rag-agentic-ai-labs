from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport, StdioTransport
from lomond import response
from mcp import stdio_client
import asyncio

http_transport = StreamableHttpTransport(
    url="https://mcp.context7.com/mcp"
)

http_client = Client(http_transport)
async def main():
    async with http_client as client:
        tools = await client.list_tools()

        response = await client.call_tool("resolve-library-id", {
            "libraryName": "fastmcp",
            "query": "I want to create a new MCP server using the fastmcp Python framework"
        })

        docs = await client.call_tool("query-docs", {
            "libraryId": "/llmstxt/gofastmcp_llms-full_txt",
            "query": "I want to fetch the code snippets and the documentation",
            "tokens": 5000
        })

        for tool in tools:
            print(
                f"""{tool.name}: \n
                {tool.description} \n
                {tool.inputSchema}""")
            print(response.content[0].text[:1000])
            print(docs.content[0].text[:500]) 
    
asyncio.run(main())