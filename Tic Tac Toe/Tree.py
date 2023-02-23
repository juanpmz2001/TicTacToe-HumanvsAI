from Node import *


class Tree ():
    def __init__(self, root ,operators):
        self.root=root
        self.operators=operators

    def printPath(self,n):
        stack = n.pathObjective()
        path = stack.copy()
        while len(stack)!=0:
            node=stack.pop()
            if node.operator is not None:
                print(f'operador:  {self.operators[node.operator]} \t estado: {node.state}')
            else:
                print(f' {node.state}')
        return path

    def reinitRoot(self):
        self.root.operator=None
        self.root.parent=None
        self.root.objective=None
        self.root.children = []
        self.root.level=0

    ## Primero a lo ancho
    def breadthFirst(self,endState):
        self.reinitRoot()
        pq=queue.Queue()
        pq.put(self.root)
        while not pq.empty():
            node=pq.get()
            children=node.getchildrens(self.operators)
            for i,child in enumerate(children):
                if child is not None:
                    newChild=node.add_child(value=node.value+'-'+str(i), state=child, operator=i)
                    pq.put(newChild)
                    if endState==child:
                        return newChild


    ## Primero a lo profundo
    def dephFirst(self, endState):
        self.reinitRoot()
        pq=[]
        pq.append(self.root)    
        while len(pq)>0:
            node=pq.pop()
            if (node.parent is not None):
                node.parent.add_node_child(node)
            children=node.getchildrens(self.operators)
            temp=[]
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node)
                    temp.append(newChild)
                    if endState==child:
                        node.add_node_child(newChild)
                        return newChild
        #Adicionar los hijos en forma inversa para que salga primero el primero que se adicionó
            temp.reverse()
            for e in temp:
                pq.append(e)

    ## Por costo
    def costFirst(self,endState):
        self.reinitRoot()
        pq=queue.PriorityQueue()
        pq.put((self.root.cost(), self.root))
        while not pq.empty():
            node=pq.get()[1]
            children=node.getchildrens(self.operators)
            for i,child in enumerate(children):
                if child is not None:
                    newChild=node.add_child(value=node.value+'-'+str(i), state=child, operator=i)
                    pq.put((newChild.cost(), newChild))
                    if endState==child:
                        return newChild

    ## Primero el mejor 
    def bestFirst(self,endState):
        self.reinitRoot()
        pq=queue.PriorityQueue()
        pq.put((self.root.heuristic(),self.root))
        while not pq.empty():
            node=pq.get()[1]
            children=node.getchildrens()
            for i,child in enumerate(children):
                if child is not None:
                    newChild=node.add_child(value=node.value+'-'+str(i), 
                                            state=child, operator=i)
                    pq.put((newChild.heuristic(),newChild))
                    if endState==child:
                        return newChild

    ## A*
    def Aasterisk(self,endState):
        self.reinitRoot()
        pq=queue.PriorityQueue()
        pq.put((self.root.f(),self.root))
        while not pq.empty():
            node=pq.get()[1]
            children=node.getchildrens()
            for i,child in enumerate(children):
                if child is not None:
                    newChild=node.add_child(value=node.value+'-'+str(i), 
                                            state=child, operator=i)
                    pq.put((newChild.f(),newChild))
                    if endState==child:
                        return newChild

        ## Generar los hijos del nodo 
        
    def miniMax(self, depth):
        self.root.v=self.miniMaxR(self.root, depth, True)
        ## Comparar los hijos de root
        values=[c.v for c in self.root.children]
        maxvalue=max(values)
        index=values.index(maxvalue)
        return self.root.children[index]

    def miniMaxR(self, node, depth, maxPlayer):
        if depth==0 or node.isObjective():
            node.v=node.heuristic()
            return node.heuristic()
        ## Generar los hijos del nodo
        children=node.getchildrens(self.operators)
        
        ## Según el jugador que sea en el árbol
        if maxPlayer:
            value=float('-inf')
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node, 
                                            operators=node.operators,player=False)
                    newChild=node.add_node_child(newChild)
                    value=max(value,self.miniMaxR(newChild,depth-1,False))
        #node.v=value
        #return value
        else:
            value=float('inf')
            for i,child in enumerate(children):
                if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node,
                                            operators=node.operators,player=True)
                    newChild=node.add_node_child(newChild)
                    value=min(value,self.miniMaxR(newChild,depth-1,True))
        node.v=value
        return value    

    def alphabeta(self, node, depth, alpha, beta, player):
        if depth == 0 or node.isObjective():
            return node.heuristic()
            
        if player:
            value = float('-inf')
            for i, child in enumerate(node.getchildrens(self.operators)):
                 if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node, 
                                            operators=node.operators,player=False)
                    newChild=node.add_node_child(newChild)
                    value = max(value, self.alphabeta(newChild, depth - 1, node.alpha, node.beta, False))
                    node.alpha = max(node.alpha, value)
                    if node.alpha >= node.beta:
                        break
                    node.v = value
            return value
        else:
            value = float('inf')
            for i, child in enumerate(node.getchildrens(self.operators)):
                 if child is not None:
                    newChild=type(self.root)(value=node.value+'-'+str(i),state=child,operator=i,parent=node, 
                                            operators=node.operators,player=False)
                    newChild=node.add_node_child(newChild)
                    value = max(value, self.alphabeta(newChild, depth - 1, node.alpha, node.beta, False))
                    node.alpha = max(node.alpha, value)
                    if node.alpha >= node.beta:
                        break
                    node.v = value
            return value   
    
    def sAlphaBeta(self, depth = 6):
        self.root.v = self.alphabeta(self.root, depth, float('-inf'), float('inf'), True)
        ## Comparar los hijos de root
        values = [c.v for c in self.root.children]
        print(values)
        value=max(values)
        i=values.index(value)
        return self.root.children[i]

    def draw(self,path):
        graph = pydot.Dot(graph_type='graph')
        nodeGraph=pydot.Node(str(self.root.state)+"-"+str(0),
                            label=str(self.root.state),shape ="circle", 
                            style="filled", fillcolor="red")
        graph.add_node(nodeGraph)
        path.pop()
        return self.drawTreeRec(self.root,nodeGraph,graph,0,path.pop(),path)
        
    def drawTreeRec(self,r,rootGraph,graph,i,topPath,path):
        if r is not None:
            children=r.children
            for j,child in enumerate(children):
                i=i+1
                color="white"
                if topPath.value==child.value:
                    if len(path)>0:topPath=path.pop()
                    color='red'
                c=pydot.Node(child.value,label=str(child.state)+r"\n"+r"\n"+"f="+str(child.f()), 
                            shape ="circle", style="filled", 
                            fillcolor=color)
                graph.add_node(c)
                graph.add_edge(pydot.Edge(rootGraph, c, 
                                        label=str(child.operator)+'('+str(child.cost())+')'))
                graph=self.drawTreeRec(child,c,graph,i,topPath,path)  # recursive call
            return graph
        else:
            return graph
