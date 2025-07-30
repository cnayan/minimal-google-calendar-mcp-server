from textwrap import dedent
from fastmcp import FastMCP
from platform import system, release

from GCalendarAPI import GCalendarAPI

os=system()
version=release()

instructions=dedent(f'''
Google Calendar MCP server provides tools to interact directly with the user's Google Calendar.
''')

mcp = FastMCP("Google-Calendar-MCP",instructions=instructions)
gcal = GCalendarAPI()

@mcp.tool("get-events", description="Gets specified numebr of upcoming events from Google Calendar. If number is not specified, defaults to 10.")
def get_events(num: int = 10) -> list[dict[str, object]]:
    return gcal.get(num)

def main():
    
    mcp.run()

if __name__ == "__main__":
    main()
