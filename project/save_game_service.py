from typing import Dict, List, Optional

from pydantic import BaseModel


class SaveGameStateResponse(BaseModel):
    """
    Provides feedback on the attempt to save the game state, indicating success or the nature of any failure.
    """

    success: bool
    message: str
    gameStateId: Optional[str] = None


async def save_game(
    userId: str, mapState: Dict, playerPosition: Dict[str, int], inventory: List[str]
) -> SaveGameStateResponse:
    """
    Saves the current game state for the player, including map and player-specific data.

    Args:
        userId (str): Identifier for the user whose game state is being saved.
        mapState (Dict): A JSON object representing the current state of the map, including cell types, items, NPCs, and other relevant configurations.
        playerPosition (Dict[str, int]): Coordinates marking the player's current position on the map.
        inventory (List[str]): List of items currently in the player's inventory, captured as a list of item identifiers.

    Returns:
        SaveGameStateResponse: Provides feedback on the attempt to save the game state, indicating success or the nature of any failure.
    """
    try:
        import prisma.models

        user_exists = await prisma.models.User.prisma().find_unique(
            where={"id": userId}
        )
        if not user_exists:
            return SaveGameStateResponse(
                success=False, message=f"No user found with ID: {userId}"
            )
        game_state = await prisma.models.GameState.prisma().create(
            data={
                "userId": userId,
                "data": {
                    "mapState": mapState,
                    "playerPosition": playerPosition,
                    "inventory": inventory,
                },
            }
        )
        if game_state:
            return SaveGameStateResponse(
                success=True,
                message="Game state saved successfully.",
                gameStateId=game_state.id,
            )
        else:
            return SaveGameStateResponse(
                success=False, message="Failed to save game state."
            )
    except Exception as e:
        return SaveGameStateResponse(
            success=False,
            message=f"An error occurred while saving the game state: {str(e)}",
        )
