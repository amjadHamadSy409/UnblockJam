

import copy as cp
from state_management import StateManagement
import termcolor as tc
from movement_checker import MovementChecker as mch
class Movement:
   
   
   
  def move_to_new_cells(grid, block, direction, steps, state_manager=None):
        direction = direction.lower() 
        new_grid = cp.deepcopy(grid)
        current_block = new_grid.all_blocks[block.id]
        
        if not block.is_movable:
            return False, f"This {block.type} cannot move "
        
        dx, dy = 0, 0   
        if direction == 'u': 
            dx, dy = -1, 0 
        elif direction == 'd': 
            dx, dy = 1, 0 
        elif direction == 'r': 
            dx, dy = 0, 1
        elif direction == 'l': 
            dx, dy = 0, -1
        else: 
            return False, f"Direction '{direction}' is not valid."
        
        current_position = list(current_block.position)      
        temporary_new_positions = [] 
        
        
        for step in range(1, steps + 1):
            temporary_new_positions = []
            for x, y in current_position:
                new_x = x + (dx * step)
                new_y = y + (dy * step)
                temporary_new_positions.append((new_x, new_y))
            
            
            for new_x, new_y in temporary_new_positions:       
                
                if 0 <= new_x < new_grid.row and 0 <= new_y < new_grid.column:
                    new_cell = new_grid.block_reference[new_x][new_y]
                    
                    if new_cell is not None and new_cell.id != current_block.id:
                        if new_cell.type == 'piece' or new_cell.type == 'block':
                            return False, f"Cannot jump over {new_cell.type} at ({new_x},{new_y}) at step {step}."
                        
                        elif new_cell.type == 'gate' and new_cell.color != current_block.color:
                            return False, f"Cannot pass non-matching gate at ({new_x},{new_y}) at step {step}."
                else:
                    continue    
        
        
            final_new_positions = temporary_new_positions
        
       
        is_exit_move = False
        target_gate = None
        
        for new_x, new_y in final_new_positions:
            if 0 <= new_x < new_grid.row and 0 <= new_y < new_grid.column:
                new_cell = new_grid.block_reference[new_x][new_y]
                if new_cell is not None and new_cell.type == 'gate' :
                    is_exit_move = True
                    target_gate = new_cell
           
        
        if is_exit_move and target_gate:
            
            success, result = mch.move_to_excited(new_grid, target_gate, current_block, final_new_positions)
            if success:
                if state_manager:
                    state_manager.add_state(new_grid)
               
                return True,(result,"Piece exited successfully!")
            else:
                return False, result
        else:
            
            success, result = mch.move_to_cell_None(new_grid, current_block, final_new_positions)
            if success:
                if state_manager:
                    state_manager.add_state(new_grid)
                return True, new_grid
            else:
                return False, result







































     
       