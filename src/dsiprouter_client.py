import httpx
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class DSIPRouterClient:
    def __init__(self, base_url: str, token: str, verify_ssl: bool = True):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.verify_ssl = verify_ssl
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[dict] = None,
        json_data: Optional[dict] = None
    ) -> dict[str, Any]:
        url = f"{self.base_url}/api/v1{endpoint}"
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_kamailio_stats(self) -> dict[str, Any]:
        return await self._request("GET", "/kamailio/stats")
    
    async def reload_kamailio(self) -> dict[str, Any]:
        return await self._request("POST", "/reload/kamailio")

    async def get_endpoint_lease(self, ttl: int, email: str) -> dict[str, Any]:
        return await self._request("GET", "/endpoint/lease", params={"ttl": ttl, "email": email})
    
    async def revoke_endpoint_lease(self, lease_id: int) -> dict[str, Any]:
        return await self._request("PUT", f"/endpoint/lease/{lease_id}/revoke")

    async def list_carrier_groups(self) -> dict[str, Any]:
        return await self._request("GET", "/carriergroups")
    
    async def get_carrier_group(self, gwgroupid: int) -> dict[str, Any]:
        return await self._request("GET", f"/carriergroups/{gwgroupid}")
    
    async def create_carrier_group(self, data: dict) -> dict[str, Any]:
        return await self._request("POST", "/carriergroups", json_data=data)
    
    async def update_carrier_group(self, gwgroupid: int, data: dict) -> dict[str, Any]:
        return await self._request("PUT", f"/carriergroups/{gwgroupid}", json_data=data)
    
    async def delete_carrier_group(self, gwgroupid: int) -> dict[str, Any]:
        return await self._request("DELETE", f"/carriergroups/{gwgroupid}")

    async def list_endpoint_groups(self) -> dict[str, Any]:
        return await self._request("GET", "/endpointgroups")
    
    async def get_endpoint_group(self, groupid: int) -> dict[str, Any]:
        return await self._request("GET", f"/endpointgroups/{groupid}")
    
    async def create_endpoint_group(self, data: dict) -> dict[str, Any]:
        return await self._request("POST", "/endpointgroups", json_data=data)
    
    async def update_endpoint_group(self, groupid: int, data: dict) -> dict[str, Any]:
        return await self._request("PUT", f"/endpointgroups/{groupid}", json_data=data)
    
    async def delete_endpoint_group(self, groupid: int) -> dict[str, Any]:
        return await self._request("DELETE", f"/endpointgroups/{groupid}")

    async def list_inbound_mappings(self) -> dict[str, Any]:
        return await self._request("GET", "/inboundmapping")
    
    async def get_inbound_mapping(self, ruleid: int) -> dict[str, Any]:
        return await self._request("GET", f"/inboundmapping/{ruleid}")
    
    async def create_inbound_mapping(self, data: dict) -> dict[str, Any]:
        return await self._request("POST", "/inboundmapping", json_data=data)
    
    async def update_inbound_mapping(self, ruleid: int, data: dict) -> dict[str, Any]:
        return await self._request("PUT", f"/inboundmapping/{ruleid}", json_data=data)
    
    async def delete_inbound_mapping(self, did: str) -> dict[str, Any]:
        return await self._request("DELETE", "/inboundmapping", params={"did": did})

    async def get_cdrs_by_endpoint_group(self, endpointgroup: str) -> dict[str, Any]:
        return await self._request("GET", f"/cdrs/endpointgroups/{endpointgroup}")
