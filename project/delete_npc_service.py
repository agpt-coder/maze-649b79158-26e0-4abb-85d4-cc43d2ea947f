import prisma
import prisma.models
from pydantic import BaseModel


class DeleteNPCResponse(BaseModel):
    """
    Response model confirming the deletion of an NPC.
    """

    message: str


async def delete_npc(npcId: str) -> DeleteNPCResponse:
    """
    Remove an NPC from the game environment.

    This function deletes an NPC using its unique identifier from the ProjectMap's NPCs list.
    After successful deletion, it returns a response model confirming the deletion.

    Args:
        npcId (str): The unique identifier of the NPC to be deleted.

    Returns:
        DeleteNPCResponse: A model containing a message confirming the NPC's successful deletion.

    Example:
        response = await delete_npc('npc_uuid')
        print(response)
        > {"message": "NPC with ID npc_uuid has been successfully deleted."}
    """
    await prisma.models.NPC.prisma().delete(where={"id": npcId})
    return DeleteNPCResponse(
        message=f"NPC with ID {npcId} has been successfully deleted."
    )
