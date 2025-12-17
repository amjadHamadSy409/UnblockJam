import copy
from grid import Grid
from movement import Movement
from state_management import StateManagement
import termcolor as tc
import time
from solver import Solver
class Game:
    
 @staticmethod 
 def move_block_action(grid: Grid, block_id: int, direction: str,steps: int, state_manager: StateManagement) -> bool:
   
    direction = direction.lower()
    block_to_move = grid.all_blocks.get(block_id)
    
    if not block_to_move or not block_to_move.is_movable:
        print(tc.colored(f" Error: Block {block_id} not found or is not movable.", 'red'))
        return False
        

    success, result = Movement.move_to_new_cells(grid, block_to_move, direction,steps, state_manager)
    
    if success:

        if isinstance(result, Grid):
            new_grid = result
            

            grid.block_reference = new_grid.block_reference
            grid.movable_pieces = new_grid.movable_pieces
            grid.all_blocks = new_grid.all_blocks
            grid.row = new_grid.row 
            grid.column = new_grid.column 
            
            print(tc.colored(f" Block {block_id} moved {direction} successfully.", 'green'))
        
        else:

            updated_grid_state = state_manager.get_current_state()
            if updated_grid_state:
                
                grid.block_reference = updated_grid_state.block_reference
                grid.movable_pieces = updated_grid_state.movable_pieces
                grid.all_blocks = updated_grid_state.all_blocks
            
            print(tc.colored(f" Piece {block_id} exited the grid successfully. ({result})", 'green'))
            
        return True
    else:
        print(tc.colored(f" Cannot move block {block_id} {direction}. Reason: {result}", 'red'))
        return False
    
    
 def run_interface(grid, state_manager,  StateManagement, move_block_action):

        print(tc.colored("\n--- Puzzle Game Interface ---", 'cyan', attrs=['bold']))
        
        while True:
            print("\n" + "="*40)
            
          
            print("Current Grid State:")
            grid.display()

          
            for p in grid.movable_pieces:
            
              print(f"\nMovable Pieces IDs: {p.id} and Position: {p.position} and Colors: {p.color}  ")
             
            frozen_pieces=[b for b in grid.all_blocks.values() if b.type=='piece' and hasattr(b,'freeze_count') and b.freeze_count>0]  
            
            if frozen_pieces:
                print(tc.colored("\n--- FROZEN Pieces (Cannot Move) ---", 'magenta', attrs=['bold']))
                for p in frozen_pieces:
                    print(f"ID: {p.id} | Pos: {p.position} | Color: {p.color}")
                    print(tc.colored(f"    -> ❄️  FROZEN: Remaining moves to unfreeze: {p.freeze_count}", 'cyan'))
            
            if not grid.movable_pieces:
                print(tc.colored("\n CONGRATULATIONS! All pieces have exited the grid!", 'yellow', attrs=['bold']))
                break

          
            prompt = "Enter move (e.g., ID direction steps: '1 right 3', '7 up 5'), 'undo', or 'exit',or 'restart' : "
            user_input = input(prompt).strip().lower()

            if user_input == 'exit':
                print(tc.colored(" Exiting game.", 'yellow'))
                break
            
            if user_input == 'restart':
                init_grid = state_manager.restart()
                if init_grid:
                    
                    grid.__dict__.update(init_grid.__dict__)
                    print(tc.colored(" Game restarted to the initial state.", 'blue'))
                else:
                    print(tc.colored(" Restart failed: Initial state not found.", 'red'))
                continue
            
            if user_input == 'undo':
                previous_grid = state_manager.undo()
                if previous_grid:
                    
                    grid.__dict__.update(previous_grid.__dict__)
                    print(tc.colored(" Undid the last move.", 'green'))
                else:
                    print(tc.colored(" Cannot undo. Already at the initial state.", 'yellow'))
                continue
            
            
            try:
                parts = user_input.split()
                if len(parts) == 3:
                    
                    piece_id = int(parts[0])
                    direction = parts[1]
                    steps = int(parts[2])
                elif len(parts) == 2:
                    
                    piece_id = int(parts[0])
                    direction = parts[1]
                    steps = 1 
                else:
                    
                    raise ValueError("Incorrect number of arguments. Use 'ID direction steps' (e.g., '1 right 3'), 'ID direction', 'undo', or 'exit'.")
                
                Game.move_block_action(grid, piece_id, direction,steps, state_manager)
                
            except ValueError as e:
                print(tc.colored(f" Invalid command. Please check ID and direction. Error: {e}", 'red'))
            except Exception as e:
                print(tc.colored(f" An unexpected error occurred: {e}", 'red'))
                
                
                
                
class GameController:
    
    @staticmethod
    def print_algorithm_stats(algo_name, solution_path, nodes_expanded, elapsed_time):
        
        print(tc.colored(f"\n{'='*50}", 'blue'))
        
        print(tc.colored(f"Algorithm Results: {algo_name}", 'green', attrs=['bold']))
        print(tc.colored(f"{'='*50}", 'blue'))

        if solution_path:
            
            print(f"Elapsed Time: {tc.colored(f'{elapsed_time:.4f} seconds', 'yellow')}")
            
            print(f"Total Nodes Expanded: {tc.colored(nodes_expanded, 'cyan')}")
           
            print(f"Solution Path Length: {tc.colored(len(solution_path), 'cyan')}")
            
           
            print(tc.colored("\nSolution Path:", 'white', attrs=['bold']))
            for i, move in enumerate(solution_path):
                
                block_id, direction, steps = move[0], move[1], move[2]
                action = f"Move Block {block_id} {direction.upper()} {steps} step(s)"
                if len(move) == 4 and move[3] == "EXIT":
                    
                    action += tc.colored(" (EXIT)", 'magenta', attrs=['bold'])
                print(f"   [{i+1}] {action}")
        else:

            print(tc.colored("No solution found.", 'red'))
            
            print(f"Time: {elapsed_time:.4f} seconds")
            
            print(f"Nodes Expanded: {nodes_expanded}")
        print(tc.colored(f"{'='*50}\n", 'blue'))
        
        
    
    
    
    @staticmethod
    def start_game(initial_grid):
       
        while True:
           
            print(tc.colored("\nSelect Play Mode:", 'cyan', attrs=['bold']))
            
            print("1. Manual Play")
           
            print("2. BFS Algorithm")
           
            print("3. DFS Algorithm (Iterative)")
            
            print("4. DFS Algorithm (Recursive)")
            
            print("5. UCS Algorithm (Uniform Cost Search)")
           
            print("0. Exit")
            
            
            choice = input(tc.colored(" choices> ", 'yellow')).strip()
            
            
            grid_copy = copy.deepcopy(initial_grid)
            
            if choice == '1':
                
                state_manager = StateManagement(grid_copy)
                
                Game.run_interface(
                   grid=grid_copy, 
                   state_manager=state_manager, 
                            StateManagement=StateManagement,
                            move_block_action=Game.move_block_action
                        )
    
                
            elif choice == '2':
               
                print("Running BFS...")
                start = time.time()
                path, nodes = Solver.solve_puzzle_bfs(grid_copy)
                elapsed = time.time() - start
                GameController.print_algorithm_stats("BFS", path, nodes, elapsed)
                
            elif choice == '3':
                
                print("Running DFS (Iterative)...")
                start = time.time()
                path, nodes = Solver.solve_puzzle_dfs(grid_copy)
                elapsed = time.time() - start
                GameController.print_algorithm_stats("DFS Iterative", path, nodes, elapsed)
                
            elif choice == '4':
                
                print("Running DFS (Recursive)...")
                start = time.time()
                path, nodes = Solver.solve_puzzle_dfs_recursive(grid_copy)
                elapsed = time.time() - start
                GameController.print_algorithm_stats("DFS Recursive", path, nodes, elapsed)
                
            elif choice == '5': 
                print("Running UCS...")
                start = time.time()
                
                path, nodes = Solver.solve_puzzle_ucs(grid_copy)
                elapsed = time.time() - start
                GameController.print_algorithm_stats("UCS (Cost: steps moved)", path, nodes, elapsed)
                
            elif choice == '0':
                
                print("Goodbye!")
                break
            else:
                
                print(tc.colored("Invalid choice, try again.", 'red'))