
from timeit import main
import grid as g

from play_game import Game , GameController

GRID_FILE='field-1.1.json'
game_grid=g.Grid.create_grid_from_json(GRID_FILE)

if game_grid:
    print(f"grid created in size {game_grid.row}x{game_grid.column}") 
    game_grid.display()
    GameController.start_game(game_grid)
else:
    print("Failed to create grid from the provided JSON file.")