import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=300)
import pandas as pd
import time
from PIL import Image
from Node import *

class astar():

    def findPath(self, map):                                        #Kjorer A-star paa en map som inneholder start og maal-posisjoner
        Open = []
        Closed = []
        stateDict = {}                                              #Dictionary med nodene som allerde er opprettet

        startnode = node(map.start_pos)                             #Gjor klar startnoden
        startnode.set_g(0)
        startnode.set_h(self.manhattan(startnode.pos, map.goal_pos))

        Open.append(startnode)


        while len(Open) != 0:                                      #Selve A-star loopen

            X = Open.pop(0)                                        #Poppe noden med lavest f fra Open
            Closed.append(X)

            if X.pos == map.end_goal_pos:                           #Nar sluttnode er oppdaget, returner denne
                print("HALLELUJA! Maalnode X funnet!")
                return X

            Children = []
            for tuple in [(0,1),(1,0),(0,-1),(-1,0)]:                               #Genererer barnenoder
                child = node([X.x + tuple[0], X.y + tuple[1]])
                if map.get_cell_value(child.pos) in [1,2,3,4] :                     #Sjekker at barnenoden er gyldig, feks. ikke er utenfor tillatt omrade (cell_value = -1)
                    Children.append(child)
            
            for child in Children:                                                  #Se gjennom de genererte barna
                currentChild = child
                if (child.x,child.y) in stateDict.keys():
                    currentChild = stateDict.get((child.x,child.y))                 #Sjekk stateDict om barnenoden allerde er opprettet. I saa fall, bruk den i stedet

                X.children.append(currentChild)                                     #Legger til gyldig barnenode i foreldrenodens children-liste

                if not currentChild in Open and not currentChild in Closed :        #Evaluerer barnet
                    self.attach_and_eval(map,currentChild,X)
                    Open.append(currentChild)
                    Open.sort(key=lambda x: x.f)                                    #Sorterer Open
                elif (X.g + self.arc_cost(map,currentChild)) <  currentChild.g :
                    self.attach_and_eval(map,currentChild,X)
                    if currentChild in Closed:
                        self.propagate_path_improvements(currentChild)

                stateDict[(currentChild.x,currentChild.y)] = currentChild           #Opprettede noder settes inn i dictionary

        raise Exception("FAIL. Ingen maalnode X funnet")


    def attach_and_eval(self, map, child, parent):                       #Setter "parent" som child sin parent (attach) og beregner childs g og h (evaluate)
        child.parent = parent
        child.set_g(parent.g + self.arc_cost(map,child))
        child.set_h(self.manhattan(child.pos,map.goal_pos))

    def propagate_path_improvements(self,parent):                        #Dersom det oppdages en raksere vei til parent, oppdateres g-verdien til alle dens barn
        for child in parent.children :
            if (parent.g + self.arc_cost(map,child)) < child.g :
                child.parent = parent
                child.set_g(parent.g + self.arc_cost(map,child))
                self.propagate_path_improvements(child)


    def arc_cost(self,map,node):
        return map.get_cell_value(node.pos)

    def manhattan(self,pos1, pos2):                             #Beregner manhattan distanse til maal-posisjon, til bruk i estimert avstand (h)
        return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

    def print_path(self, map, node):                            #Gaar gjennom og printer hvor en node og alle dens barn er på en map. Brukes nar maal-noden er funnet og ruten skal printes
        map.set_cell_value(node.pos,'G')
        if not(node.parent is None):
            self.print_path(map,node.parent)
    