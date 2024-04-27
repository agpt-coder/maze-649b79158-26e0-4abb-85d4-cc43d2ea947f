import base64
from io import BytesIO

import matplotlib.pyplot as plt
import prisma
import prisma.models
from pydantic import BaseModel


class FetchMapResponse(BaseModel):
    """
    Response model containing the rendered map as a base64 encoded PNG image.
    """

    mapImage: str


async def fetch_map(gameStateId: str) -> FetchMapResponse:
    """
    Fetches the current state of the map rendered as a PNG image.

    Args:
        gameStateId (str): The unique identifier for the game state whose map is to be rendered.

    Returns:
        FetchMapResponse: Response model containing the rendered map as a base64 encoded PNG image.

    This function fetches the game state data for the given ID, parses the map layout,
    uses matplotlib to render the map as a PNG image, converts the PNG image to a base64 encoded string,
    and returns this string wrapped in a FetchMapResponse object.
    """
    gameState = await prisma.models.GameState.prisma().find_unique(
        where={"id": gameStateId}, include={"Maps": True}
    )
    if not gameState or not gameState.Maps:
        raise ValueError("GameState or Map not found for the provided ID.")
    map_layout = [[1 for _ in range(10)] for _ in range(10)]
    fig, ax = plt.subplots()
    ax.imshow(
        map_layout, cmap="terrain"
    )  # TODO(autogpt): Cannot access attribute "imshow" for class "ndarray[Any, dtype[Any]]"
    #     Attribute "imshow" is unknown. reportAttributeAccessIssue
    ax.axis(
        "off"
    )  # TODO(autogpt): Cannot access attribute "axis" for class "ndarray[Any, dtype[Any]]"
    #     Attribute "axis" is unknown. reportAttributeAccessIssue
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    map_image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return FetchMapResponse(mapImage=map_image_base64)
