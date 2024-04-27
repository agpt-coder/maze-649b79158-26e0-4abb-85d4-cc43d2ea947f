from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class NPCResponse(BaseModel):
    """
    The response of the NPC creation process containing either the details of the newly created NPC or a description of the error encountered.
    """

    success: bool
    npc_id: Optional[str] = None
    message: Optional[str] = None


async def create_npc(
    name: str, description: Optional[str], attributes: Dict, projectMapId: str
) -> NPCResponse:
    """
    Create a new NPC with specified behaviors and attributes.

    Args:
    name (str): The name of the NPC.
    description (Optional[str]): A brief description or backstory for the NPC.
    attributes (Dict): A JSON blob containing various attributes defining the NPC's behavior, appearance, stats, or other customizable characteristics.
    projectMapId (str): ID of the map where the NPC is initially placed. This links the NPC to a specific location within the game's world.

    Returns:
    NPCResponse: The response of the NPC creation process containing either the details of the newly created NPC or a description of the error encountered.
    """
    try:
        existing_project_map = await prisma.models.ProjectMap.prisma().find_unique(
            where={"id": projectMapId}
        )
        if not existing_project_map:
            return NPCResponse(
                success=False,
                message=f"ProjectMap with ID {projectMapId} does not exist.",
            )
        created_npc = await prisma.models.NPC.prisma().create(
            data={
                "name": name,
                "description": description,
                "attributes": attributes,
                "projectMapId": projectMapId,
            }
        )
        return NPCResponse(
            success=True, npc_id=created_npc.id, message="NPC created successfully."
        )
    except Exception as e:
        print(f"Failed to create NPC: {str(e)}")
        return NPCResponse(
            success=False, message="An error occurred while creating the NPC."
        )
