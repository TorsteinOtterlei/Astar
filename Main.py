from Map import Map_Obj
from Node import *
from Astar import *


class main():
    map = Map_Obj(4)                #Oppretter map-objekt(oppgavenr)
    astar = astar()                 #Oppretter astar-objekt

    X = astar.findPath(map)         #Finner X, maalnoden med foreldrenodene som gir beste løsning
    astar.print_path(map, X)        #Printer ruten på kartet

    map.show_map()                  #Viser kartet med rute

