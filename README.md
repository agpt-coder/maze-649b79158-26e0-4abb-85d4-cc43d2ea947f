---
date: 2024-04-27T16:00:25.566340
author: AutoGPT <info@agpt.co>
---

# maze 6

To create a simple Python map game with a Flask API that includes a 2D map grid, cells with different values indicating unknown areas, floors, walls, doors, starting points, and endpoints, along with configurable items and NPCs in cells, the recommended tech stack involves Python for programming, Flask as the API framework, and Matplotlib for displaying the map as a PNG file. The game's architecture involves a grid implemented as a list of lists, where each cell's value represents its type (unknown, floor, wall, door, start point, end point). Items within the game would have a base model meta description allowing for customization at instantiation, and although NPCs can exist in any cell, interacting with them would raise a 'NotImplemented' exception. For creating medium and small rooms with corridors of 1 or 2 cells in width, careful design and planning of the grid are required, resembling the layout found in games like Pokémon but accessible through an API. This setup encourages exploring different areas of the map, configuring items, and eventually saving or displaying the map using Matplotlib, which adds a visual component to the game's API.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'maze 6'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
