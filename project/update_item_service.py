from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdatedItemType(BaseModel):
    """
    A detailed view of the item after an update operation, showing its current state.
    """

    itemId: str
    name: str
    description: str
    metaData: Dict[str, Any]


class ItemUpdateResponse(BaseModel):
    """
    Confirms the successful update of an item, returning the updated attributes for verification by the client.
    """

    success: bool
    updatedItem: UpdatedItemType


async def update_item(
    itemId: str, name: str, description: Optional[str], metaData: Dict[str, Any]
) -> ItemUpdateResponse:
    """
    Update attributes of an existing item.

    Args:
    itemId (str): The unique identifier for the item being updated.
    name (str): The updated name of the item.
    description (Optional[str]): The updated description or lore attached to the item.
    metaData (Dict[str, Any]): A JSON structure containing updated metadata for the item, including effects, appearance changes, and any other custom attributes.

    Returns:
    ItemUpdateResponse: Confirms the successful update of an item, returning the updated attributes for verification by the client.
    """
    item_to_update = await prisma.models.Item.prisma().find_unique(where={"id": itemId})
    if item_to_update is None:
        return ItemUpdateResponse(success=False, updatedItem=None)
    updated_item = await prisma.models.Item.prisma().update(
        where={"id": itemId},
        data={"name": name, "description": description, "metaData": metaData},
    )
    updated_item_type = UpdatedItemType(
        itemId=updated_item.id,
        name=updated_item.name,
        description=updated_item.description,
        metaData=updated_item.metaData,
    )
    return ItemUpdateResponse(success=True, updatedItem=updated_item_type)
