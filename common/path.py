#
# OpenRTS - Copyright (C) 2006 The OpenRTS Project
#
# OpenRTS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# OpenRTS is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# Pathfinding based on AStar by John Eriksson.
# Released as public domain, and released under the GPL 
# with permission from author. 
# See: http://arainyday.se/projects/python/AStar/ 

from threading import Thread
import logging
from time import time

#****************************************************************************
#
#****************************************************************************
class Path:
    def __init__(self,nodes, totalCost):
        self.nodes = nodes;
        self.totalCost = totalCost;

    def getNodes(self): 
        return self.nodes    

    def getTotalMoveCost(self):
        return self.totalCost

#****************************************************************************
#
#****************************************************************************
class Node:
    def __init__(self,tile,mCost,lid,parent=None):
        self.tile = tile # where is this node located
        self.mCost = mCost # total move cost to reach this node
        self.parent = parent # parent node
        self.score = 0 # calculated score for this node
        self.lid = lid # set the tile id - unique for each tile in the map

    def __eq__(self, n):
        if n.lid == self.lid:
            return 1
        else:
            return 0
#****************************************************************************
# Pathfinding using the A* alorithm.
# Important:
# The pathfinding is run in a separate thread from the main game
# and will update the path-attribute of the unit if pathfinding
# succeeds.
#****************************************************************************
class AStar(Thread):

    def __init__(self, unit, game_state, start_tile, end_tile):
        Thread.__init__(self)
        self.mh = game_state.map;
        self.game_state = game_state;
        self.unit = unit;
        self.start_tile = start_tile;
        self.end_tile = end_tile;

#****************************************************************************
# Start the actual pathfinding, and update unit path attribute when done.
#****************************************************************************
    def run(self):
      start_time = time();
      node_path = self.find_path(self.start_tile, self.end_tile);         
      if node_path and self.unit:
        self.unit.path = [];
        for node in node_path.getNodes():
          self.unit.path.append((node.tile.x, node.tile.y));
        self.game_state.netclient.send_unit_path(self.unit.id, self.unit.path);
      else:
        logging.info("No path found"); 
      print("Found path in %r seconds" % (time() - start_time));

    def _getBestOpenNode(self):
        bestNode = None        
        for n in self.on:
            if not bestNode:
                bestNode = n
            else:
                if n.score<=bestNode.score:
                    bestNode = n
        return bestNode

    def _tracePath(self,n):
        nodes = [];
        totalCost = n.mCost;
        p = n.parent;
        nodes.insert(0,n);       
        
        while 1:
            if p.parent is None: 
                break

            nodes.insert(0,p)
            p=p.parent
        
        return Path(nodes,totalCost)

    def _handleNode(self,node,end):        
        i = self.o.index(node.lid)
        self.on.pop(i)
        self.o.pop(i)
        self.c.append(node.lid)

        nodes = self.mh.get_adjacent_nodes(node, end, self.unit)
                   
        for n in nodes:
            if n.tile == end:
                # reached the destination
                return n
            elif n.lid in self.c:
                # already in close, skip this
                continue
            elif n.lid in self.o:
                # already in open, check if better score
                i = self.o.index(n.lid)
                on = self.on[i];
                if n.mCost<on.mCost:
                    self.on.pop(i);
                    self.o.pop(i);
                    self.on.append(n);
                    self.o.append(n.lid);
            else:
                # new node, append to open list
                self.on.append(n);                
                self.o.append(n.lid);

        return None

    def find_path(self,fromtile, totile):
        self.o = []
        self.on = []
        self.c = []

        end = totile
        fnode = self.mh.get_node(fromtile, self.unit)
        self.on.append(fnode)
        self.o.append(fnode.lid)
        nextNode = fnode 
               
        while nextNode is not None: 
            finish = self._handleNode(nextNode,end)
            if finish:                
                return self._tracePath(finish)
            nextNode=self._getBestOpenNode()
        return None

