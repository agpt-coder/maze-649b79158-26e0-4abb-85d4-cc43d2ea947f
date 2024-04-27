from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class NPC(BaseModel):
    """
    A detailed representation of an NPC, including its attributes and behaviors.
    """

    id: str
    name: str
    description: str
    attributes: Dict[str, Any]


class UpdateNpcResponse(BaseModel):
    """
    Response structure confirming the NPC's updated status.
    """

    success: bool
    npc: NPC


async def update_npc(
    name: Optional[str],
    description: Optional[str],
    attributes: Dict[str, Any],
    npcId: str,
) -> UpdateNpcResponse:
    """
    Update the attributes or behaviors of an existing NPC.

    Args:
        name (Optional[str]): The new name for the NPC.
        description (Optional[str]): A new description for the NPC.
        attributes (Dict[str, Any]): A JSON structure representing the updated attributes and behaviors of the NPC.
        npcId (str): The unique identifier of the NPC to be updated.

    Returns:
        UpdateNpcResponse: Response structure confirming the NPC's updated status.
    """
    npc = await prisma.models.NPC.prisma().find_unique(where={"id": npcId})
    if npc is None:
        return UpdateNpcResponse(
            success=False, npc=NPC(id="", name="", description="", attributes={})
        )
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if attributes:
        update_data["attributes"] = attributes
    updated_npc = await prisma.models.NPC.prisma().update(
        where={"id": npcId}, data=update_data
    )
    npc_updated = NPC(
        id=updated_npc.id,
        name=updated_npc.name,
        description=updated_npc.description,
        attributes=updated_npc.attributes,
    )
    return UpdateNpcResponse(success=True, npc=npc_updated)
