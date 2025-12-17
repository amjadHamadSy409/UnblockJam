from movement import Movement
import copy
from grid import Grid
from block import Block
from collections import deque
import heapq
class Solver:
    
    
    # def generate_successors(current_grid: Grid):
    #     next_states = []
        
      
    #     directions = ['u', 'd', 'l', 'r'] 
    #     max_steps = max(current_grid.row, current_grid.column) 
        
    #     for piece in current_grid.movable_pieces:
            
    #         if not piece.is_movable and piece.freeze_count > 0:
    #            continue
          
    #         for direction in directions:
                
                
    #             max_valid_steps = 0 
    #             exit_result = None 
                
                
    #             for steps in range(1, max_steps): 
                    
    #                 temp_grid = copy.deepcopy(current_grid)
                    
    #                 if piece.id not in temp_grid.all_blocks:
    #                      continue
                         
    #                 block_in_temp = temp_grid.all_blocks[piece.id]
                    
    #                 success, result = Movement.move_to_new_cells(temp_grid, block_in_temp, direction, steps)
                    
    #                 if success:
    #                     max_valid_steps = steps
                        
    #                     if isinstance(result, tuple):
                            
    #                         exit_result = result
    #                         break 
                       
    #                 else:
                        
    #                     break
                        
               
    #             if max_valid_steps > 0:
                    
    #                 if exit_result:
                        
    #                     next_grid = exit_result[0]
    #                     move = (piece.id, direction, max_valid_steps, "EXIT")
    #                     next_states.append((next_grid, move))
                        
    #                 else:
                        
    #                     final_grid = copy.deepcopy(current_grid)
    #                     final_block = final_grid.all_blocks[piece.id]
                        
    #                     success, result = Movement.move_to_new_cells(final_grid, final_block, direction, max_valid_steps)
                        
    #                     if success and isinstance(result, Grid):
    #                         move = (piece.id, direction, max_valid_steps)
    #                         next_states.append((result, move))
                            
    #     return next_states
    @staticmethod
    def generate_successors(current_grid: Grid):
        next_states = []
        
        directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
        steps=1
        max_steps = max(current_grid.row, current_grid.column)
        
        for piece in current_grid.movable_pieces:
            
            if not piece.is_movable and piece.freeze_count>0:
                continue
            
            for direction in directions:
                for steps in range(1,max_steps): 
                    temp_grid = copy.deepcopy(current_grid)
                    
                    block_in_temp = temp_grid.all_blocks[piece.id]
                    
                    success, result = Movement.move_to_new_cells(temp_grid, block_in_temp, direction, steps)
                    
                    if success:
                        
                        if isinstance(result, tuple):
                                
                                next_grid = result[0]
                                move = (piece.id, direction, steps, "EXIT")
                                next_states.append((next_grid, move))
                            
                            
                        elif isinstance(result, Grid):
                            
                            move = (piece.id, direction, steps)
                            next_states.append((result, move))
                        
                    else:
                        break
            
                
                        
        
            
        return next_states            
            
         
    @staticmethod
    def solve_puzzle_bfs(initial_grid: Grid):
       
        queue = deque([(initial_grid, [])])
        visited = { initial_grid.to_tuple() }
        nodes_expanded = 0

        

        while queue:
            current_grid, path = queue.popleft()
            nodes_expanded += 1
            current_grid.display()
            
            if nodes_expanded % 200 == 0 or len(path) % 1000 == 0:
                print(f"🔄 Nodes expanded: {nodes_expanded} | Path len: {len(path)} | Visited: {len(visited)} | Queue: {len(queue)}")
                
            if not current_grid.movable_pieces:
                
                print(f"✅ Solution found! Steps: {len(path)}. Expanded: {nodes_expanded}. ")
                current_grid.display()
                return path, nodes_expanded

            next_states = Solver.generate_successors(current_grid)
           
            

            for next_grid, move in next_states:
                
                
                next_state = next_grid.to_tuple()
                if next_state not in visited:
                   
                    visited.add(next_state)
                    queue.append((next_grid, path + [move]))
                       

        print()
        print(f"❌ No solution found by BFS after exploring all states. Expanded: {nodes_expanded}.")
        return None, nodes_expanded
    
    
    
    
    
    
    
    @staticmethod
    def solve_puzzle_dfs(initial_grid: Grid, limit=100):
    
    
    
        stack = [(initial_grid, [])]
        
        
        visited = {initial_grid}
        
        nodes_expanded = 0

        while stack:
            current_grid, path = stack.pop()
            nodes_expanded += 1
            current_grid.display()
            
            if len(path) >= limit:
                continue 
            
            if nodes_expanded % 200 == 0 or len(path) % 1000 == 0:
              print(f"🔄 Nodes expanded: {nodes_expanded} | Path len: {len(path)} | Visited: {len(visited)} | Queue: {len(stack)}")

            if not current_grid.movable_pieces:
                
                print(f"✅ Solution found! Steps: {len(path)}. Expanded: {nodes_expanded}. ")
                current_grid.display()
                return path, nodes_expanded
                
            
            
                
        
            next_states = Solver.generate_successors(current_grid)
            
            for next_grid, move in reversed(next_states):
                next_state = next_grid.to_tuple()
                if next_state not in visited:
                    visited.add(next_state)
                    new_path = path + [move]
                    stack.append((next_grid, new_path))
                    
        return None, nodes_expanded
    
    
    
   
    @staticmethod
    def solve_puzzle_dfs_recursive(initial_grid: Grid):
        visited = {initial_grid}
        stats = {'nodes_expanded': 0}
        
        solution_path = Solver._dfs_helper(initial_grid, tuple(), visited,stats)
    
        return solution_path, stats['nodes_expanded']
    
    
    
    @staticmethod
    def _dfs_helper(current_grid: Grid, path: tuple, visited: set,stats, limit=100):
        
        current_state = current_grid.to_tuple()
        stats['nodes_expanded'] += 1
        current_grid.display()
        if current_state in visited:
            return None
        
        visited.add(current_state)
        if len(path) >= limit:
           return None, stats['nodes_expanded']
        if stats['nodes_expanded'] % 200 == 0 or len(path) % 1000 == 0:
              print(f"🔄 Nodes expanded: {stats['nodes_expanded']} | Path len: {len(path)} | Visited: {len(visited)} | stack: {stats['nodes_expanded']}")
       
        if not current_grid.movable_pieces:
                
                print(f"✅ Solution found! Steps: {len(path)}. Expanded: {stats['nodes_expanded']}. ")
                current_grid.display()
                return path

        
        next_states = Solver.generate_successors(current_grid)
        
        for next_grid, move in next_states:
            
            
            new_path = path + (move,) 
            
            
            result = Solver._dfs_helper(next_grid, new_path, visited,stats)
            
           
            if result is not None:
                return result

        
        return None
    
    
    
    
    
    @staticmethod
    def solve_puzzle_ucs(initial_grid: Grid):
       
        tie_breaker = 0
       
        priority_queue = [(0, tie_breaker, initial_grid, [])] 
        
       
        visited_costs = {initial_grid.to_tuple(): 0}
        
        nodes_expanded = 0

        while priority_queue:

            current_cost,_, current_grid, path = heapq.heappop(priority_queue)
            nodes_expanded += 1
            current_grid.display()
            
            if nodes_expanded % 200 == 0 or len(path) % 1000 == 0:
                print(f"Nodes expanded: {nodes_expanded} | Cost: {current_cost} | Visited: {len(visited_costs)} | Queue size: {len(priority_queue)}")
            
           
            if not current_grid.movable_pieces:
                print(f"Solution found! Steps: {len(path)}. Expanded: {nodes_expanded}. Total Cost: {current_cost}")
                current_grid.display()
                return path, nodes_expanded

            
            next_states = Solver.generate_successors(current_grid)
            
            for next_grid, move in next_states:
                
               
                move_steps = move[2] 
                
               
                new_cost = current_cost + move_steps 
                
                next_state_tuple = next_grid.to_tuple()
                
                
                if next_state_tuple not in visited_costs or new_cost < visited_costs[next_state_tuple]:
                    
                   
                    visited_costs[next_state_tuple] = new_cost
                    
                    
                    new_path = path + [move]
                    tie_breaker += 1
                   
                    heapq.heappush(priority_queue, (new_cost, tie_breaker, next_grid, new_path))
                    
        print(f"No solution found by UCS after exploring all states. Expanded: {nodes_expanded}.")
        return None, nodes_expanded