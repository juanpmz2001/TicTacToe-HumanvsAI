import pydot
from IPython.display import Image, display
import queue
import numpy as np

class Node ():
    def __init__(self, state,value,operators = None,operator=None, parent=None,objective=None, alpha = float('-inf'), beta= float('inf')):
        self.state= state
        self.value = value
        self.children = []
        self.parent=parent
        self.operator=operator
        self.objective=objective
        self.level=0
        self.operators=operators
        self.v=0
        self.alpha = alpha
        self.beta = beta

        
    def add_child(self, value, state, operator):
        node=type(self)(value=value, state=state, operator=operator,parent=self,operators=self.operators)
        node.level=node.parent.level+1
        self.children.append(node)
        return node
    
    def add_node_child(self, node):
        node.level=node.parent.level+1
        self.children.append(node)    
        return node

    #Devuelve todos los estados según los operadores aplicados
    def getchildrens(self, operators):
        return [
            self.getState(i) 
                if not self.repeatStatePath(self.getState(i)) 
                    else None for i, op in enumerate(self.operators)]
        
    def getState(self, index):
        pass
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __lt__(self, other):
        return self.f() < other.f()
    
    
    def repeatStatePath(self, state):
        n=self
        while n is not None and n.state!=state:
            n=n.parent
        return n is not None
        
    def pathObjective(self):
        n=self
        result=[]
        while n is not None:
            result.append(n)
            n=n.parent
        return result
  
    def cost(self):
        return 1
    
    def f(self): 
        print(self.heuristic())
        return self.cost()+self.heuristic()

    def heuristic(self):
        return 0
    ### Crear método para criterio objetivo
    ### Por defecto vamos a poner que sea igual al estado objetivo, para cada caso se puede sobreescribir la función
    def isObjective(self):
        return self.state==self.objetive.state