import json
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateItemOutput(BaseModel):
    """
    Provides confirmation details of the newly created item, including a unique identifier for reference in future interactions or updates.
    """

    itemId: str
    status: str
    message: Optional[str] = None


async def create_item(
    name: str,
    description: str,
    appearance: str,
    effects: str,
    placementConstraints: str,
    projectMapId: str,
) -> CreateItemOutput:
    """
    Create a new item with specified attributes in the database and returns confirmation details.

    Args:
        name (str): The name of the item.
        description (str): A brief description of the item and its effects.
        appearance (str): Details regarding the item's appearance within the game.
        effects (str): The effects this item has when used or interacted with, stored as a JSON formatted string detailing effect types and magnitudes.
        placementConstraints (str): Constraints on where this item can be placed on the map, expressed in JSON format.
        projectMapId (str): The unique identifier of the map where the item is initially placed.

    Returns:
        CreateItemOutput: Provides confirmation details of the newly created item, including a unique identifier for reference in future interactions or updates.
    """
    try:
        metaData = json.dumps(
            {
                "effects": json.loads(effects),
                "appearance": appearance,
                "placementConstraints": json.loads(placementConstraints),
            }
        )
        item = await prisma.models.Item.prisma().create(
            {
                "name": name,
                "description": description,
                "projectMapId": projectMapId,
                "metaData": metaData,
            }
        )
        return CreateItemOutput(
            itemId=item.id,
            status="success",
            message="prisma.models.Item created successfully.",
        )
    except Exception as e:
        return CreateItemOutput(itemId="", status="failed", message=str(e))
