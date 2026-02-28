import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["calculator_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool("add", {"a": 10, "b": 5})
            print("Add:", result.content[0].text)

            result = await session.call_tool("subtract", {"a": 10, "b": 5})
            print("Subtract:", result.content[0].text)

            result = await session.call_tool("multiply", {"a": 10, "b": 5})
            print("Multiply:", result.content[0].text)

            result = await session.call_tool("divide", {"a": 10, "b": 5})
            print("Divide:", result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())