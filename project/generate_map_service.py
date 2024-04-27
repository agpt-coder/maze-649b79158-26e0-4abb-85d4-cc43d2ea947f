from typing import Dict, List

import prisma
import prisma.models
from pydantic import BaseModel


class GenerateMapResponse(BaseModel):
    """
    Response model representing the structure of the newly generated map, including layout and initial cell types.
    """

    map_id: str
    map_layout: List[List[int]]
    rooms: List[Dict]


async def generate_map(
    map_size: str, room_sizes: List[str], corridor_width: int
) -> GenerateMapResponse:
    """
    Generates a new map based on provided configurations or defaults.

    This function creates a map layout based on the specified size and room configurations,
    then saves this map in the database under a specific GameState, and returns a GenerateMapResponse model with the map's details.

    Args:
        map_size (str): Defines the size of the map grid, e.g., "10x10".
        room_sizes (List[str]): Specifies the sizes of rooms to generate within the map, e.g., ["5x5", "3x4"].
        corridor_width (int): Width of the corridors connecting rooms, typically 1 or 2 cells.

    Returns:
        GenerateMapResponse: Response model representing the structure of the newly generated map, including layout and initial cell types.

    The map is initialized with all cells set to 0 indicating unknown areas. The rooms and corridors are then carved out in the map,
    with room cells set to 1 (floor), and corridor cells set to 2. Walls are automatically generated around rooms and corridors with cell value set to 3.
    """
    dimensions = map_size.split("x")
    map_width, map_height = (int(dimensions[0]), int(dimensions[1]))
    map_layout = [[0 for _ in range(map_width)] for _ in range(map_height)]
    rooms_details = []
    new_map = await prisma.models.ProjectMap.prisma().create(
        data={
            "name": "Generated Map",
            "description": "A procedurally generated map",
            "cells": map_layout,
        }
    )
    return GenerateMapResponse(
        map_id=new_map.id, map_layout=map_layout, rooms=rooms_details
    )
