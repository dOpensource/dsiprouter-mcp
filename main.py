#!/usr/bin/env python3
import argparse
from src.server import mcp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="dSIPRouter MCP Server")
    parser.add_argument("--http", action="store_true", help="Start the server in HTTP mode (streamable-http transport)")
    
    args = parser.parse_args()
    
    if args.http:
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
