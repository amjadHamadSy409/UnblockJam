import termcolor as tc


class MovementChecker:
   

        
    
    @staticmethod
    def move_to_cell_None(grid, block, new_positions):
       
       current_position=block.position
       
       block.position=new_positions 
       
       for new_x,new_y in block.position:
              if not (0 <= new_x < grid.row and 0 <= new_y < grid.column):

                  return False, f"Movement out of bounds detected at ({new_x}, {new_y})."
       
       for x,y in current_position:
            if 0 <= x < grid.row and 0 <= y < grid.column:  
              grid.block_reference[x][y]=None
           
       
       for new_x,new_y in block.position:
          
              grid.block_reference[new_x][new_y]=block
              
              
       return True,grid  
    
    @staticmethod
    def move_to_excited(grid,gate,current_block,final_new_positions):
           
           same_color=False
           
           check_excited=False
           
           if gate.color!=current_block.color:
                  return False,f"this gate in position {gate.position} not in that color with piece" 
           
           elif gate.color==current_block.color:
                  same_color=True
           
           
           piece_x = [x for x, y in final_new_positions] 
           piece_y = [y for x, y in final_new_positions]

           gate_x = [x for x, y in gate.position]
           gate_y = [y for x, y in gate.position]

           
           
           min_x_piece, max_x_piece = min(piece_x), max(piece_x)
           min_y_piece, max_y_piece = min(piece_y), max(piece_y)

           
           min_x_target, max_x_target = min(gate_x), max(gate_x)
           min_y_target, max_y_target = min(gate_y), max(gate_y)

            

           if min_x_target == 0 or max_x_target == grid.row - 1:
                 
                 if (min_y_piece >= min_y_target and max_y_piece <= max_y_target):
                        check_excited = True
                 else:
                    return False, "Piece is not aligned with the gate width (Y-axis mismatch)."

            
           elif min_y_target == 0 or max_y_target == grid.column - 1:

                 if (min_x_piece >= min_x_target and max_x_piece <= max_x_target):
                    check_excited = True
                 else:
                          return False, "Piece is not aligned with the gate height (X-axis mismatch)."

           else:
                   return False, "This gate location is invalid for exit."
           
           if same_color and check_excited :
               for x, y in current_block.position:
                 if 0 <= x < grid.row and 0 <= y < grid.column:
                   if grid.block_reference[x][y]==current_block  :
                        grid.block_reference[x][y] = None
                        
                        
                  
                    
                    
                              
               unfrozen_pieces = []
               for block_id, block in grid.all_blocks.items():
                 if block.type == 'piece' and block.freeze_count > 0:          
                          was_unfrozen = block.decrease_freeze() 
                        
                          if was_unfrozen:
                                unfrozen_pieces.append(block)
                                if block not in grid.movable_pieces:
                                    grid.movable_pieces.append(block)
                                
                                
               grid.movable_pieces = [p for p in grid.movable_pieces if p.id != current_block.id]

               if current_block.id in grid.all_blocks:
                     grid.all_blocks.pop(current_block.id)
                     message = f"Piece {current_block.id} exited successfully!"
                     if unfrozen_pieces:
                            unfrozen_ids = [p.id for p in unfrozen_pieces]
                            message += f"\n🎉 Frozen pieces {unfrozen_ids} are now unfrozen and can move!"
                            print(message) 
                                 

           return True,grid
    