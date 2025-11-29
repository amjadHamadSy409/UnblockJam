
import grid as g
from state_management import StateManagement
from play_game import Game as p
from block import Block
GRID_FILE='field-1.1.json'
game_grid=g.Grid.create_grid_from_json(GRID_FILE)

if game_grid:
    print(f"grid created in size {game_grid.row}x{game_grid.column}") 
    game_grid.display()
    
    state_manager = StateManagement(game_grid)


    p.run_interface(
        grid=game_grid, 
        state_manager=state_manager, 
        g=g,
        StateManagement=StateManagement,
        move_block_action=p.move_block_action
    )