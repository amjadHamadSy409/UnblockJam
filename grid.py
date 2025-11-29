import json
from block import Block
from termcolor import colored
class Grid:
    
    def __init__(self,row,column):
        self.row=row
        self.column=column
        
        self.block_reference=[[None for _ in range(column)] for _ in range(row)]
        
        self.movable_pieces=[]
        
        self.all_blocks={} 
        
    def   __eq__(self,other):
        
        if not isinstance(other,Grid):
            return False
        
        if self.row !=other.row or self.column != other.column:
            return False
        
        self_movable_pos = {tuple(sorted(p.position)) for p in self.movable_pieces}
        other_movable_pos={tuple(sorted(p.position))for p in other.movable_pieces}
        
        if self_movable_pos != other_movable_pos:
            return False
        
        for i in range(self.row):
            for j in range(self.column):
               b1= self.block_reference[i][j]
               b2= other.block_reference[i][j]
               if b1 is None and b2 is not None:
                   return False
               if b1 is not None and b2 is None :
                   return False
               if b1 is not None and b2 is not None:
                    if b1.is_movable != b2.is_movable or  b1.type != b2.type:
                        return False
               if not b1.is_movable and b1.id != b2.id:

                    return False
    
        return True
    
    
    def __hash__(self):
        
        movable_positions_tuples=[]
        for piece in self.movable_pieces:
            sorted_positions=tuple(sorted(piece.position))
            movable_positions_tuples.append(sorted_positions)
        final_hash_data=tuple(sorted(movable_positions_tuples))
        return hash((self.row,self.column,final_hash_data))
    
    
    @classmethod
    def create_grid_from_json(cls,json_file_path):
        try:
            with open (json_file_path,'r')as f:
                data=json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {json_file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {json_file_path}")
            return None
        
        rows=data.get("rows") 
        cols=data.get("cols")
        if rows is None or cols is None:
            print("Error: JSON missing 'rows' or 'cols' information.")
            return None
        grid=cls(rows,cols)
        
        shapes_data = data.get("shapes", [])
        pieces = []
        for shape in shapes_data:
            
            color_id=shape.get("colors")
            coordinates=shape.get("coordinates")
            direction = shape.get("direction", "full")
            freeze_count=shape.get("move_lock",0)
            if coordinates and color_id:
                block = Block(coordinates, color_id, 'piece','◼', direction,freeze_count)
                pieces.append(block)
            

        exists_data = data.get("exists", [])
        gates = []
        for exist in exists_data:
            color_id = exist.get("color")
            coordinates = exist.get("coordinates")
            
            if coordinates and color_id:
                block = Block(coordinates, color_id, 'gate','G')
                gates.append(block)
                
                
                
        blocks_data = data.get("blocks", [])
        fixed_blocks = []
        for coord in blocks_data:
          block = Block([coord], 0, 'block','B')
          fixed_blocks.append(block)   
        
        
        all_blocks = pieces + gates + fixed_blocks
        grid.add_block(all_blocks)
        
        Block.counter = 0
        return grid       












    def add_block(self,blocks):
       
     for block in blocks:
        self.all_blocks[block.id] = block
        if block.is_movable:
            self.movable_pieces.append(block)
        if block.type=='gate' :
            for x, y in block.position:
                
             if not(0<=x<self.row and 0<=y<self.column):
                 print("The coordinates of the point are out of bounds.")
                 continue
             
             if self.block_reference[x][y] is not None:
                 print(f"The celles ({x},{y}) is busy")
                 continue
             
             if x not in [0,self.row-1] and y not in [0,self.column-1]:
                 print(f"The ({x},{y}) cannot be placed in this location because it is a gate cell.")
                 continue
               
                        
             
             self.block_reference[x][y] = block
        if block.type =="block":
                for x,y in block.position:
                    
                     if not(0<=x<self.row and 0<=y<self.column):
                        print("The coordinates of the point are out of bounds.")
                        continue
                    
                     if self.block_reference[x][y] is not None:
                        print(f"The celles ({x},{y}) is busy")
                        continue
                    
                    
                     self.block_reference[x][y] = block
        if block.type =="piece":
                for x,y in block.position:
                    
                     if not(0<=x<self.row and 0<=y<self.column):
                        print("The coordinates of the point are out of bounds.")
                        continue
                    
                     if self.block_reference[x][y] is not None:
                        print(f"The celles ({x},{y}) is busy")
                        continue
                     if x not in range(1,self.row-1) or y not in range(1,self.column-1):
                        print(f"The ({x},{y}) cannot be placed in this location because it is a piece cell.")
                        continue
                    
                         
                  
                     self.block_reference[x][y] = block
            
                        
                    
    def display(self):
        for i in range(self.row):
            for j in range(self.column):
                cell_content = self.block_reference[i][j]
                
               
                if cell_content is not None:
                   
                    print(cell_content.shap, end=" ")
                else:
                    
                    print(".", end=" ")
            print()