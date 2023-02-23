from Node import *

class NodeTicTacToe(Node):
  ## Vamos a añadir el jugador, pues en dependencia del jugador se hace una cosa u otra.

    def __init__(self, player=True,**kwargs):
        super().__init__(**kwargs)
        self.player=player
        if player:
            self.v=float('-inf')
        else:
            self.v=float('inf')
  
    def getState(self, index):
        state=self.state
        nextState=None
        (x,y)=self.operators[index]
        if state[x][y]==' ':
            nextState= [f.copy() for f in state]
            if self.player==True: ## Si es Max se pone X    
                nextState[x][y]='X'
            else: ## Si es Max se pone X
                nextState[x][y]='O'
        return nextState if state!=nextState else None

  #Costo acumulativo(valor 1 en cada nivel)
    def cost(self):
        return self.level
  
  ##Ver si el nodo es un nodo objetivo para O o para X, o hay empate
    def isObjective(self):
        a=[f.copy() for f in self.state]
        b=np.array(a).T
        a.append(np.diag(self.state))
        a.append(np.flipud(self.state).diagonal())
        a=np.array(a)
        c=np.concatenate((a,b),axis=0)
        for f in c:
            if f[0]!=' ' and all(x == f[0] for x in f):
                return True
        ### Empate
        if not np.in1d([' '], self.state):
            return True
        return False   

  ## Si es nodo objetivo, si X retornamos 1, si O -1 y si no 0
    def heuristic(self):
        
        # Creacion arreglo a de posibilidades
        a=[f.copy() for f in self.state]
        b=np.array(a).T
        a.append(np.diag(self.state.copy()))
        a.append(np.flipud(self.state.copy()).diagonal())
        a=np.array(a)
        c=np.concatenate((a,b),axis=0)

        
        for p in c:
            if p[0]!=' ' and all(x == p[0] for x in p):
                if p[0]=='X':
                    return float('inf')
                return float('-inf')
        ## Empate
        if not np.in1d([' '], self.state):
            return 0
        ## Elaborar resto de heurística...
        
        aux = 0 #esto lo puso jp
        for p in c:
            if sum(np.char.count(p, 'X')) == 2 and not np.in1d(['O'], p):
                aux+=1
            elif sum(np.char.count(p, 'O')) == 2 and not np.in1d(['X'], p):
                aux-=1

            if np.in1d(['X'], p) and not (np.in1d(['O'], p)):
                aux+=1
            elif np.in1d(['O'], p) and not (np.in1d(['X'], p)):
                aux-=1

        return aux

    def heuristic2(self):
        
        # Creacion arreglo a de posibilidades
        a=[f.copy() for f in self.state]
        b=np.array(a).T
        a.append(np.diag(self.state.copy()))
        a.append(np.flipud(self.state.copy()).diagonal())
        a=np.array(a)
        c=np.concatenate((a,b),axis=0)

        h = 0

        for p in c:
            sumx = sum(np.char.count(p, 'X'))
            sumo = sum(np.char.count(p, 'O'))
            if sumx == 2:
                return 50
            elif sumo == 2:
                return -50
            else:
                sumb = sum(np.char.count(p, ' '))
                if sumx == 1 and sumb == 2:
                    h += 1
                if sumo == 1 and sumb == 2:
                    h -= 1
        
        return h

        








    #def heuristic():
        # gane?
        # me ganaron?
        # mis_posibilidades-posibilidades_del_contrario