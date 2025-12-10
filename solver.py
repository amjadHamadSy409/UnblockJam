from movement import Movement
import copy
from grid import Grid
from block import Block
from collections import deque
class Solver:
    
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

            # print progress occasionally
            if nodes_expanded % 200 == 0 or len(path) % 1000 == 0:
                print(f"🔄 Nodes expanded: {nodes_expanded} | Path len: {len(path)} | Visited: {len(visited)} | Queue: {len(queue)}")

            # check goal: no movable pieces
            if not current_grid.movable_pieces:
                
                print(f"✅ Solution found! Steps: {len(path)}. Expanded: {nodes_expanded}. ")
                current_grid.display()
                return path

            next_states = Solver.generate_successors(current_grid)
           
            

            for next_grid, move in next_states:
                
                
                next_state = next_grid.to_tuple()
                if next_state not in visited:
                   
                    visited.add(next_state)
                    queue.append((next_grid, path + [move]))
                       

        print()
        print(f"❌ No solution found by BFS after exploring all states. Expanded: {nodes_expanded}.")
        return None
    
    
    
    
    
    
    
    @staticmethod
    def solve_puzzle_dfs(initial_grid: Grid, limit=100):
    
    
    
        stack = [(initial_grid, [])]
        
        
        visited = {initial_grid}
        
        nodes_expanded = 0

        while stack:
            current_grid, path = stack.pop()
            nodes_expanded += 1
            
            
            if len(path) >= limit:
                continue 
            
            if nodes_expanded % 200 == 0 or len(path) % 1000 == 0:
              print(f"🔄 Nodes expanded: {nodes_expanded} | Path len: {len(path)} | Visited: {len(visited)} | Queue: {len(stack)}")

            if not current_grid.movable_pieces:
                
                print(f"✅ Solution found! Steps: {len(path)}. Expanded: {nodes_expanded}. ")
                current_grid.display()
                return path
                
            
            
                
        
            next_states = Solver.generate_successors(current_grid)
            
            for next_grid, move in reversed(next_states):
                next_state = next_grid.to_tuple()
                if next_state not in visited:
                    visited.add(next_state)
                    new_path = path + [move]
                    stack.append((next_grid, new_path))
                    
        return None
    
    
    
   
    @staticmethod
    def solve_puzzle_dfs_recursive(initial_grid: Grid):
        visited = {initial_grid}
        stats = {'nodes_expanded': 0}
        # استدعاء التابع المساعد
        solution_path = Solver._dfs_helper(initial_grid, tuple(), visited,stats)
    
        return solution_path
    
    
    
    @staticmethod
    def _dfs_helper(current_grid: Grid, path: tuple, visited: set,stats, limit=100):
        
        current_state = current_grid.to_tuple()
        stats['nodes_expanded'] += 1
        # 1. حالة التوقف الأولى (إذا كانت العقدة مُزارة بالفعل)
        if current_state in visited:
            return None
        
        visited.add(current_state)
        if len(path) >= limit:
           return None
        if stats['nodes_expanded'] % 200 == 0 or len(path) % 1000 == 0:
              print(f"🔄 Nodes expanded: {stats['nodes_expanded']} | Path len: {len(path)} | Visited: {len(visited)} | stack: {stats['nodes_expanded']}")
        # 2. حالة التوقف الثانية (التحقق من الهدف)
        if not current_grid.movable_pieces:
                
                print(f"✅ Solution found! Steps: {len(path)}. Expanded: {stats['nodes_expanded']}. ")
                current_grid.display()
                return path# تم العثور على الحل

        # 3. خطوة العودية (استكشاف الجيران)
        next_states = Solver.generate_successors(current_grid)
        
        for next_grid, move in next_states:
            
            # بناء المسار الجديد للحالة اللاحقة
            new_path = path + (move,) 
            
            # 4. الاستدعاء الذاتي (التعمق في الفرع)
            result = Solver._dfs_helper(next_grid, new_path, visited,stats)
            
            # إذا أعاد الاستدعاء نتيجة غير None، فهذا هو الحل، فنمرره للأعلى.
            if result is not None:
                return result

        # 5. فشل البحث في هذا الفرع
        return None