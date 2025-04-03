import asyncio
import os
import shutil
import sys
import nest_asyncio

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServer, MCPServerStdio

from dotenv import load_dotenv
load_dotenv()



# ...existing code...

async def run(mcp_server: MCPServer):
    try:
        agent = Agent(
            name="Intelligent Assistant",
            instructions="""Use the tools to read the filesystem and answer questions based on those files.""",
            mcp_servers=[mcp_server],
        )
        
        print("Starting agent process..............................................................")

        # List the files it can read
        message = "Read the files and list them."
        print(f"Running: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
        
        message = "list books in favorite_books.txt file?"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
            
        # Ask about books
        message = "What is my #1 favorite book?"
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)

        # Ask a question that reads then reasons.
        message = "Look at my favorite songs. Suggest one new song that I might like."
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
        
        message ="Look at favorite songs file and list the songs in it."
        print(f"\n\nRunning: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
        
        print("Agent process finished..............................................................")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        raise


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as server:
        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Filesystem Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            await run(server)


if __name__ == "__main__":
    # Let's make sure the user has npx installed
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    
    # Apply nest_asyncio to fix event loop issues
    nest_asyncio.apply()
    
    asyncio.run(main())