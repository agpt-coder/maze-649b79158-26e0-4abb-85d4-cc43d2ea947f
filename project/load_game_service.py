import json
from typing import Any, Dict, List

import prisma
import prisma.models
from pydantic import BaseModel


class LoadGameStateResponse(BaseModel):
    """
    Provides the loaded game state data, allowing the player to resume their game from where they left off. Includes the map state, player position, inventory items, and any other relevant game details contained in the saved state.
    """

    gameStateId: str
    userId: str
    mapState: List[List[int]]
    inventoryItems: List[Dict[str, Any]]
    playerPosition: Dict[str, int]


async def load_game(gameStateId: str) -> LoadGameStateResponse:
    """
    Loads a previously saved game state.

    Args:
        gameStateId (str): The unique identifier of the game state to be loaded.

    Returns:
        LoadGameStateResponse: Provides the loaded game state data, allowing the player to resume their game from where they left off. Includes the map state, player position, inventory items, and any other relevant game details contained in the saved state.
    """
    game_state = await prisma.models.GameState.prisma().find_unique(
        where={"id": gameStateId},
        include={"Maps": {"include": {"Items": True, "NPCs": True}}},
    )
    if game_state is None:
        raise ValueError("Game state not found")
    data = json.loads(game_state.data)
    map_state = data["mapState"] if "mapState" in data else []
    player_position = data["playerPosition"] if "playerPosition" in data else {}
    inventory_items = [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "metaData": item.metaData,
        }
        for map in game_state.Maps
        for item in map.Items
    ]
    response = LoadGameStateResponse(
        gameStateId=game_state.id,
        userId=game_state.userId,
        mapState=map_state,
        inventoryItems=inventory_items,
        playerPosition=player_position,
    )
    return response
