import prisma
import prisma.models
from pydantic import BaseModel


class DeleteItemResponse(BaseModel):
    """
    This model provides feedback on the result of the delete operation, including any success or error messages.
    """

    success: bool
    message: str


async def delete_item(itemId: str) -> DeleteItemResponse:
    """
    Remove an item from the game.

    Args:
    itemId (str): The unique identifier of the item to be deleted.

    Returns:
    DeleteItemResponse: This model provides feedback on the result of the delete operation, including any success or error messages.
    """
    try:
        item = await prisma.models.Item.prisma().delete(where={"id": itemId})
        if item:
            return DeleteItemResponse(
                success=True, message=f"Item with ID {itemId} was successfully deleted."
            )
        else:
            return DeleteItemResponse(
                success=False, message=f"Item with ID {itemId} not found."
            )
    except Exception as e:
        return DeleteItemResponse(success=False, message=str(e))
