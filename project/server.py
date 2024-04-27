import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

import project.create_item_service
import project.create_npc_service
import project.delete_item_service
import project.delete_npc_service
import project.fetch_map_service
import project.generate_map_service
import project.load_game_service
import project.login_user_service
import project.logout_user_service
import project.register_user_service
import project.save_game_service
import project.update_item_service
import project.update_npc_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="maze 6",
    lifespan=lifespan,
    description="To create a simple Python map game with a Flask API that includes a 2D map grid, cells with different values indicating unknown areas, floors, walls, doors, starting points, and endpoints, along with configurable items and NPCs in cells, the recommended tech stack involves Python for programming, Flask as the API framework, and Matplotlib for displaying the map as a PNG file. The game's architecture involves a grid implemented as a list of lists, where each cell's value represents its type (unknown, floor, wall, door, start point, end point). Items within the game would have a base model meta description allowing for customization at instantiation, and although NPCs can exist in any cell, interacting with them would raise a 'NotImplemented' exception. For creating medium and small rooms with corridors of 1 or 2 cells in width, careful design and planning of the grid are required, resembling the layout found in games like Pokémon but accessible through an API. This setup encourages exploring different areas of the map, configuring items, and eventually saving or displaying the map using Matplotlib, which adds a visual component to the game's API.",
)


@app.delete(
    "/item/{itemId}/delete",
    response_model=project.delete_item_service.DeleteItemResponse,
)
async def api_delete_delete_item(
    itemId: str,
) -> project.delete_item_service.DeleteItemResponse | Response:
    """
    Remove an item from the game.
    """
    try:
        res = await project.delete_item_service.delete_item(itemId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/logout", response_model=project.logout_user_service.LogoutResponse)
async def api_post_logout_user(
    session_token: str,
) -> project.logout_user_service.LogoutResponse | Response:
    """
    Log out the current user, invalidating the session token.
    """
    try:
        res = await project.logout_user_service.logout_user(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/item/create", response_model=project.create_item_service.CreateItemOutput)
async def api_post_create_item(
    name: str,
    description: str,
    appearance: str,
    effects: str,
    placementConstraints: str,
    projectMapId: str,
) -> project.create_item_service.CreateItemOutput | Response:
    """
    Create a new item with specified attributes.
    """
    try:
        res = await project.create_item_service.create_item(
            name, description, appearance, effects, placementConstraints, projectMapId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/register", response_model=project.register_user_service.RegisterUserResponse
)
async def api_post_register_user(
    email: str, password: str
) -> project.register_user_service.RegisterUserResponse | Response:
    """
    Register a new user with email and password.
    """
    try:
        res = await project.register_user_service.register_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/game/save", response_model=project.save_game_service.SaveGameStateResponse)
async def api_post_save_game(
    userId: str, mapState: Dict, playerPosition: Dict[str, int], inventory: List[str]
) -> project.save_game_service.SaveGameStateResponse | Response:
    """
    Saves the current game state for the player, including map and player-specific data.
    """
    try:
        res = await project.save_game_service.save_game(
            userId, mapState, playerPosition, inventory
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/npc/{npcId}/delete", response_model=project.delete_npc_service.DeleteNPCResponse
)
async def api_delete_delete_npc(
    npcId: str,
) -> project.delete_npc_service.DeleteNPCResponse | Response:
    """
    Remove an NPC from the game environment.
    """
    try:
        res = await project.delete_npc_service.delete_npc(npcId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/npc/{npcId}/update", response_model=project.update_npc_service.UpdateNpcResponse
)
async def api_put_update_npc(
    name: Optional[str],
    description: Optional[str],
    attributes: Dict[str, Any],
    npcId: str,
) -> project.update_npc_service.UpdateNpcResponse | Response:
    """
    Update the attributes or behaviors of an existing NPC.
    """
    try:
        res = await project.update_npc_service.update_npc(
            name, description, attributes, npcId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.login_user_service.UserLoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.UserLoginResponse | Response:
    """
    Authenticate a user, returning a session token.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/item/{itemId}/update",
    response_model=project.update_item_service.ItemUpdateResponse,
)
async def api_put_update_item(
    itemId: str, name: str, description: Optional[str], metaData: Dict[str, Any]
) -> project.update_item_service.ItemUpdateResponse | Response:
    """
    Update attributes of an existing item.
    """
    try:
        res = await project.update_item_service.update_item(
            itemId, name, description, metaData
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/npc/create", response_model=project.create_npc_service.NPCResponse)
async def api_post_create_npc(
    name: str, description: Optional[str], attributes: Dict, projectMapId: str
) -> project.create_npc_service.NPCResponse | Response:
    """
    Create a new NPC with specified behaviors and attributes.
    """
    try:
        res = await project.create_npc_service.create_npc(
            name, description, attributes, projectMapId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/map/generate", response_model=project.generate_map_service.GenerateMapResponse
)
async def api_post_generate_map(
    map_size: str, room_sizes: List[str], corridor_width: int
) -> project.generate_map_service.GenerateMapResponse | Response:
    """
    Generates a new map based on provided configurations or defaults.
    """
    try:
        res = await project.generate_map_service.generate_map(
            map_size, room_sizes, corridor_width
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/game/load/{gameStateId}",
    response_model=project.load_game_service.LoadGameStateResponse,
)
async def api_get_load_game(
    gameStateId: str,
) -> project.load_game_service.LoadGameStateResponse | Response:
    """
    Loads a previously saved game state.
    """
    try:
        res = await project.load_game_service.load_game(gameStateId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/map/{gameStateId}/render",
    response_model=project.fetch_map_service.FetchMapResponse,
)
async def api_get_fetch_map(
    gameStateId: str,
) -> project.fetch_map_service.FetchMapResponse | Response:
    """
    Fetches the current state of the map rendered as a PNG image.
    """
    try:
        res = await project.fetch_map_service.fetch_map(gameStateId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
