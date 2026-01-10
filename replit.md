# dSIPRouter MCP Server

## Overview
This is a Model Context Protocol (MCP) server that provides tools for interacting with the dSIPRouter API. It allows AI assistants to manage VoIP infrastructure including carrier groups, endpoint groups (PBXs), and inbound DID mappings.

## Project Architecture

```
/
├── main.py                 # Entry point for the MCP server
├── src/
│   ├── __init__.py
│   ├── server.py           # MCP server with all tools defined
│   └── dsiprouter_client.py # HTTP client for dSIPRouter API
├── pyproject.toml          # Python dependencies
└── replit.md               # This file
```

## Configuration

The server requires the following environment variables:

- `DSIP_BASE_URL` - Base URL of your dSIPRouter instance (e.g., `https://your-dsip-server:5000`)
- `DSIP_TOKEN` - API bearer token for authentication
- `DSIP_VERIFY_SSL` - Set to `true` to verify SSL certificates (default: `true`)

## Available MCP Tools (18 total)

### Kamailio Management
- `get_kamailio_stats` - Get SIP server statistics
- `reload_kamailio` - Reload configuration after changes

### Endpoint Lease Management
- `get_endpoint_lease` - Get a new endpoint lease
- `revoke_endpoint_lease` - Revoke an existing lease

### Carrier Group Management
- `list_carrier_groups` - List all carrier groups (SIP trunking providers)
- `get_carrier_group` - Get carrier group details
- `create_carrier_group` - Create a new carrier group
- `update_carrier_group` - Update an existing carrier group
- `delete_carrier_group` - Delete a carrier group

### Endpoint Group Management (PBX)
- `list_endpoint_groups` - List all endpoint groups (PBXs)
- `get_endpoint_group` - Get endpoint group details
- `create_endpoint_group` - Create a new endpoint group
- `update_endpoint_group` - Update an existing endpoint group
- `delete_endpoint_group` - Delete an endpoint group

### Inbound Mapping Management
- `list_inbound_mappings` - List inbound DID mappings
- `get_inbound_mapping` - Get inbound mapping details
- `create_inbound_mapping` - Create a new inbound mapping
- `update_inbound_mapping` - Update an existing inbound mapping
- `delete_inbound_mapping` - Delete an inbound mapping

### Call Detail Records
- `get_cdrs_by_endpoint_group` - Get CDRs for a specific endpoint group

## Running the Server

### STDIO Mode (Default)
```bash
python main.py
```

### HTTP/SSE Mode
```bash
python main.py --transport streamable-http --port 8000
```

## Connecting to Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "dsiprouter": {
      "command": "python",
      "args": ["/path/to/main.py"],
      "env": {
        "DSIP_BASE_URL": "https://your-dsip-server:5000",
        "DSIP_TOKEN": "your-api-token"
      }
    }
  }
}
```

## API Reference

Based on the official dSIPRouter Postman collection:
- https://www.postman.com/dopensource/dsiprouter/collection/0iuyb66/dsiprouter

## Recent Changes
- January 9, 2026: Updated to match official dSIPRouter Postman API collection
  - Renamed carriers to carriergroups
  - Renamed endpoints to endpointgroups  
  - Renamed inbound routes to inboundmapping
  - Added CDR endpoint for call records
  - Fixed reload_kamailio endpoint path
- January 8, 2026: Initial implementation of dSIPRouter MCP server
