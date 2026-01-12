import os
import json
import logging
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from src.dsiprouter_client import DSIPRouterClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DSIP_BASE_URL = os.environ.get("DSIP_BASE_URL", "https://localhost:5000")
DSIP_TOKEN = os.environ.get("DSIP_TOKEN", "")
DSIP_VERIFY_SSL = os.environ.get("DSIP_VERIFY_SSL", "true").lower() == "true"

def _split_env_list(value: str | None) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

def _transport_security_settings() -> TransportSecuritySettings:
    allowed_hosts = _split_env_list(os.getenv("MCP_ALLOWED_HOSTS"))
    allowed_origins = _split_env_list(os.getenv("MCP_ALLOWED_ORIGINS"))
    if not allowed_hosts and not allowed_origins:
        return TransportSecuritySettings(enable_dns_rebinding_protection=False)
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=allowed_hosts,
        allowed_origins=allowed_origins,
    )

mcp = FastMCP("dsiprouter-mcp",stateless_http=True,transport_security=_transport_security_settings(),)

def get_client() -> DSIPRouterClient:
    if not DSIP_TOKEN:
        raise ValueError("DSIP_TOKEN environment variable is required")
    return DSIPRouterClient(DSIP_BASE_URL, DSIP_TOKEN, DSIP_VERIFY_SSL)


@mcp.tool()
async def get_kamailio_stats() -> str:
    """Get Kamailio SIP server statistics and metrics from dSIPRouter."""
    client = get_client()
    result = await client.get_kamailio_stats()
    return json.dumps(result, indent=2)


@mcp.tool()
async def reload_kamailio() -> str:
    """Reload Kamailio configuration to apply changes. Call this after modifying carrier groups, endpoint groups, or inbound mappings."""
    client = get_client()
    result = await client.reload_kamailio()
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_endpoint_lease(ttl: int, email: str) -> str:
    """
    Get a new endpoint lease from dSIPRouter.
    
    Args:
        ttl: Time-to-live in minutes for the lease
        email: Email address associated with the lease
    """
    client = get_client()
    result = await client.get_endpoint_lease(ttl, email)
    return json.dumps(result, indent=2)


@mcp.tool()
async def revoke_endpoint_lease(lease_id: int) -> str:
    """
    Revoke an existing endpoint lease.
    
    Args:
        lease_id: The ID of the lease to revoke
    """
    client = get_client()
    result = await client.revoke_endpoint_lease(lease_id)
    return json.dumps(result, indent=2)


@mcp.tool()
async def list_carrier_groups() -> str:
    """List all carrier groups configured in dSIPRouter. Carrier groups are SIP trunking providers used for outbound calls."""
    client = get_client()
    result = await client.list_carrier_groups()
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_carrier_group(gwgroupid: int) -> str:
    """
    Get details of a specific carrier group.
    
    Args:
        gwgroupid: The gateway group ID of the carrier to retrieve
    """
    client = get_client()
    result = await client.get_carrier_group(gwgroupid)
    return json.dumps(result, indent=2)


@mcp.tool()
async def create_carrier_group(name: str, ip_addr: str, strip: int = 0, prefix: str = "") -> str:
    """
    Create a new carrier group in dSIPRouter.
    
    Args:
        name: Name for the carrier group
        ip_addr: IP address of the carrier
        strip: Number of digits to strip from dialed numbers
        prefix: Prefix to add to dialed numbers
    """
    client = get_client()
    data = {
        "name": name,
        "ip_addr": ip_addr,
        "strip": strip,
        "prefix": prefix
    }
    result = await client.create_carrier_group(data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_carrier_group(gwgroupid: int, name: str = "", ip_addr: str = "", strip: int = -1, prefix: str = "") -> str:
    """
    Update an existing carrier group in dSIPRouter. Only provided fields will be updated.
    
    Args:
        gwgroupid: The gateway group ID of the carrier to update
        name: New name for the carrier group (optional)
        ip_addr: New IP address of the carrier (optional)
        strip: Number of digits to strip (optional, -1 to skip)
        prefix: Prefix to add to dialed numbers (optional)
    """
    client = get_client()
    data = {}
    if name:
        data["name"] = name
    if ip_addr:
        data["ip_addr"] = ip_addr
    if strip >= 0:
        data["strip"] = strip
    if prefix:
        data["prefix"] = prefix
    result = await client.update_carrier_group(gwgroupid, data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def delete_carrier_group(gwgroupid: int) -> str:
    """
    Delete a carrier group from dSIPRouter.
    
    Args:
        gwgroupid: The gateway group ID of the carrier to delete
    """
    client = get_client()
    result = await client.delete_carrier_group(gwgroupid)
    return json.dumps(result, indent=2)


@mcp.tool()
async def list_endpoint_groups() -> str:
    """List all endpoint groups configured in dSIPRouter. Endpoint groups are PBX systems like FreePBX, FusionPBX, etc."""
    client = get_client()
    result = await client.list_endpoint_groups()
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_endpoint_group(groupid: int) -> str:
    """
    Get details of a specific endpoint group.
    
    Args:
        groupid: The group ID of the endpoint group to retrieve
    """
    client = get_client()
    result = await client.get_endpoint_group(groupid)
    return json.dumps(result, indent=2)


@mcp.tool()
async def create_endpoint_group(name: str, host: str, port: int = 5060, auth_type: str = "ip", description: str = "", rweight: int = 1, keepalive: int = 0, strip: int = 0, prefix: str = "", notification_email: str = "", endpointfailure_email: str = "") -> str:
    """
    Create a new endpoint group in dSIPRouter.
    
    Args:
        name: Name for the endpoint group
        host: Hostname or IP address of the endpoint
        port: Port number for the endpoint (default: 5060)
        auth_type: Authentication type - 'ip' or 'userpwd' (default: 'ip')
        description: Description for the endpoint (default: same as name)
        rweight: Relative weight for load balancing (default: 1)
        keepalive: Keepalive interval in seconds (default: 0, disabled)
        strip: Number of digits to strip from dialed numbers (default: 0)
        prefix: Prefix to add to dialed numbers (default: "")
        notification_email: Email for over max call limit notifications (default: "")
        endpointfailure_email: Email for endpoint failure notifications (default: "")
    """
    client = get_client()
    data = {
        "name": name,
        "auth": {"type": auth_type},
        "endpoints": [{
            "host": host,
            "port": port,
            "signalling": "proxy",
            "media": "proxy",
            "description": description or name,
            "rweight": rweight,
            "keepalive": keepalive
        }],
        "strip": strip,
        "prefix": prefix,
        "notifications": {
            "overmaxcalllimit": notification_email,
            "endpointfailure": endpointfailure_email
        }
    }
    result = await client.create_endpoint_group(data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_endpoint_group(groupid: int, name: str = None, host: str = None, port: int = None, auth_type: str = None, description: str = None, rweight: int = None, keepalive: int = None, strip: int = None, prefix: str = None, notification_email: str = None, endpointfailure_email: str = None) -> str:
    """
    Update an existing endpoint group in dSIPRouter. Only provided fields will be updated.
    
    Args:
        groupid: The group ID of the endpoint group to update
        name: New name for the endpoint group (optional)
        host: New hostname or IP address of the endpoint (optional)
        port: New port number for the endpoint (optional)
        auth_type: New authentication type - 'ip' or 'userpwd' (optional)
        description: New description for the endpoint (optional)
        rweight: New relative weight for load balancing (optional)
        keepalive: New keepalive interval in seconds (optional)
        strip: New number of digits to strip from dialed numbers (optional)
        prefix: New prefix to add to dialed numbers (optional)
        notification_email: Email for over max call limit notifications (optional)
        endpointfailure_email: Email for endpoint failure notifications (optional)
    """
    client = get_client()
    data = {}
    if name is not None:
        data["name"] = name
    if auth_type is not None:
        data["auth"] = {"type": auth_type}
    if host is not None:
        endpoint = {
            "host": host,
            "port": port if port is not None else 5060,
            "signalling": "proxy",
            "media": "proxy",
            "description": description if description is not None else "",
            "rweight": rweight if rweight is not None else 1,
            "keepalive": keepalive if keepalive is not None else 0
        }
        data["endpoints"] = [endpoint]
    if strip is not None:
        data["strip"] = strip
    if prefix is not None:
        data["prefix"] = prefix
    if notification_email is not None or endpointfailure_email is not None:
        notifications = {}
        if notification_email is not None:
            notifications["overmaxcalllimit"] = notification_email
        if endpointfailure_email is not None:
            notifications["endpointfailure"] = endpointfailure_email
        data["notifications"] = notifications
    result = await client.update_endpoint_group(groupid, data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def delete_endpoint_group(groupid: int) -> str:
    """
    Delete an endpoint group from dSIPRouter.
    
    Args:
        groupid: The group ID of the endpoint group to delete
    """
    client = get_client()
    result = await client.delete_endpoint_group(groupid)
    return json.dumps(result, indent=2)


@mcp.tool()
async def list_inbound_mappings() -> str:
    """List all inbound DID mappings in dSIPRouter. Inbound mappings route incoming calls to endpoint groups."""
    client = get_client()
    result = await client.list_inbound_mappings()
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_inbound_mapping(ruleid: int) -> str:
    """
    Get details of a specific inbound mapping.
    
    Args:
        ruleid: The rule ID of the inbound mapping to retrieve
    """
    client = get_client()
    result = await client.get_inbound_mapping(ruleid)
    return json.dumps(result, indent=2)


@mcp.tool()
async def create_inbound_mapping(did: str, groupid: int) -> str:
    """
    Create a new inbound DID mapping in dSIPRouter.
    
    Args:
        did: The DID (phone number) to route
        groupid: The endpoint group ID to route calls to
    """
    client = get_client()
    data = {
        "did": did,
        "servers": "#" + [str(groupid)]
    }
    result = await client.create_inbound_mapping(data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_inbound_mapping(ruleid: int, did: str = "", groupid: int = -1) -> str:
    """
    Update an existing inbound mapping in dSIPRouter. Only provided fields will be updated.
    
    Args:
        ruleid: The rule ID of the inbound mapping to update
        did: New DID (phone number) for the mapping (optional)
        groupid: New endpoint group ID to route calls to (optional, -1 to skip)
    """
    client = get_client()
    data = {}
    if did:
        data["did"] = did
    if groupid >= 0:
        data["servers"] = "#"[str(groupid)]
    result = await client.update_inbound_mapping(ruleid, data)
    return json.dumps(result, indent=2)


@mcp.tool()
async def delete_inbound_mapping(did: str) -> str:
    """
    Delete an inbound mapping from dSIPRouter.
    
    Args:
        did: The DID (phone number) of the inbound mapping to delete
    """
    client = get_client()
    result = await client.delete_inbound_mapping(did)
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_cdrs_by_endpoint_group(endpointgroup: str) -> str:
    """
    Get Call Detail Records (CDRs) for a specific endpoint group.
    
    Args:
        endpointgroup: The name or ID of the endpoint group
    """
    client = get_client()
    result = await client.get_cdrs_by_endpoint_group(endpointgroup)
    return json.dumps(result, indent=2)


@mcp.resource("config://dsiprouter")
def get_config() -> str:
    """Get current dSIPRouter connection configuration."""
    return json.dumps({
        "base_url": DSIP_BASE_URL,
        "verify_ssl": DSIP_VERIFY_SSL,
        "token_configured": bool(DSIP_TOKEN)
    }, indent=2)


@mcp.prompt()
def carrier_setup_prompt(carrier_name: str, ip_address: str) -> str:
    """Generate a prompt for setting up a new carrier group."""
    return f"""Please set up a new carrier group with the following details:
- Carrier Name: {carrier_name}
- IP Address: {ip_address}

After creating the carrier group, remember to reload Kamailio to apply the changes."""


@mcp.prompt()
def pbx_setup_prompt(pbx_name: str, ip_address: str) -> str:
    """Generate a prompt for setting up a new endpoint group (PBX)."""
    return f"""Please set up a new endpoint group with the following details:
- PBX Name: {pbx_name}
- IP Address: {ip_address}

After creating the endpoint group, remember to reload Kamailio to apply the changes."""


if __name__ == "__main__":
    mcp.run()
