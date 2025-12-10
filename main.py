
from timeit import main
import grid as g
from state_management import StateManagement
from play_game import Game as p
from block import Block
from solver import Solver
import time
import termcolor as tc
GRID_FILE='field-1.1.json'
game_grid=g.Grid.create_grid_from_json(GRID_FILE)

if game_grid:
    print(f"grid created in size {game_grid.row}x{game_grid.column}") 
    game_grid.display()
    
    state_manager = StateManagement(game_grid)


    # p.run_interface(
    #     grid=game_grid, 
    #     state_manager=state_manager, 
    #     g=g,
    #     StateManagement=StateManagement,
    #     move_block_action=p.move_block_action
    # )
    
    
    
    
    # next_state=Solver.generate_successors(game_grid)
    
    # if next_state:
    #     for grid,state in next_state:
            
    #       print (f"------ The next state due to move:{state} ----------")
    #       grid.display()
          
          
          
          
          
          
          
    start_time = time.time()
    solution_path = Solver.solve_puzzle_dfs_recursive(game_grid)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if solution_path:
        print(tc.colored(f"🎉 SUCCESS! Puzzle Solved in {len(solution_path)} moves.", 'green', attrs=['bold']))
        print(f"Time elapsed: {elapsed_time:.4f} seconds.")
        
        print("\nDetailed Solution Path:")
        print("------------------------------")
        
        for i, move in enumerate(solution_path):
            block_id, direction, steps = move[0], move[1], move[2]
            action = f"Move Block {block_id} {direction.upper()} {steps} step(s)"
            if len(move) == 4 and move[3] == "EXIT":
                action += tc.colored(" (EXIT)", 'magenta')
            print(f"[{i+1}/{len(solution_path)}] -> {action}")
                
    else:
             print(tc.colored(f"❌ No solution found by BFS after exploring all states. Time elapsed: {elapsed_time:.4f} seconds.", 'red', attrs=['bold']))
             
if __name__ == "__main__":
  main()