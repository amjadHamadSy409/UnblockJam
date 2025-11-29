from termcolor import colored
class Block:
    counter=0
    
    types=['piece','gate','block']
    COLOR_MAP = {
        1: 'red',
        2: 'green',
        3: 'yellow',
        4: 'blue',
        5: 'magenta',
        6: 'cyan',
        7: 'white',
        
    }
    
    def __init__(self,position,color_id,type,shap,orientation='full',freeze_count=0):
        Block.counter+=1
        self.id=Block.counter
        self.position=position
        self.orientation=orientation
        self.freeze_count=freeze_count
        self.color_id=color_id
        self.color=Block.COLOR_MAP.get(color_id,'light_grey')
        if type in Block.types:
         self.type=type
         
        else:
            print("This Type is not Existing")
        if shap=='B':
            self.shap=colored(shap,'black',attrs=['bold'])
        elif self.type=='piece' and self.freeze_count>0:
            self.shap=colored(shap, self.color, attrs=['bold', 'underline'])
        else:
          self.shap=colored(shap,self.color,attrs=['bold'])
        
         
        
        if (self.type=="piece" and self.freeze_count==0):
            self.is_movable=True
        else:
            self.is_movable=False
            
        
        
    def decrease_freeze(self):
        if  (self.type=="piece" and self.freeze_count>0) :
            self.freeze_count -= 1
            if self.freeze_count > 0:
                self.shap = colored('◼', self.color, attrs=['bold', 'underline'])
                return False
            else:
                self.shap = colored('◼', self.color, attrs=['bold'])
                self.is_movable = True  
                return True 
        return False    
        
        
    def get_freeze_status(self):
        
        if (self.type == 'piece'):
            if self.freeze_count == 0:
                return "UNFROZEN ✓"
            else:
                return f"FROZEN ({self.freeze_count} moves left)"
        return "N/A"
    def __repr__(self):
          return f"Block(ID:{self.id},Type:{self.type},Position:{self.position}, Freeze:{self.freeze_count})"
        
    def __eq__(self, other):
        if isinstance(other, Block):
            # مقارنة الخصائص الأساسية
            return (self.id == other.id and 
                    self.type == other.type and 
                    self.position == other.position and
                    self.freeze_count == other.freeze_count) # أضفنا التجميد للمساواة
        return False
        
        
    def __hash__(self):
            pos_tuple = tuple(tuple(p) for p in self.position)
            return hash((self.id, self.type, pos_tuple))
            