import copy
class StateManagement:
    def __init__(self, grid):
        self.grid = grid
        self.history = [copy.deepcopy(grid)]
        
        
    def add_state(self, grid):
        
        self.history.append(copy.deepcopy(grid))
    
    def undo(self):
        
        if len(self.history) > 1:
            self.history.pop()
            return self.history[-1]
        return None
    
    def get_current_state(self):
       
        return self.history[-1] if self.history else None
    def restart(self):
        return self.history[0]