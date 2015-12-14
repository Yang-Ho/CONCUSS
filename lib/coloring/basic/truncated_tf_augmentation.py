#!/usr/bin/python
#
# This file is part of CONCUSS, https://github.com/theoryinpractice/concuss/, and is
# Copyright (C) North Carolina State University, 2015. It is licensed under
# the three-clause BSD license; see LICENSE.
#



from lib.util.memorized import memorized
from lib.graph.graph import Graph

import sys

# Calculate one transitive-fraternal-augmentation-step and
# result a tuple (newgraph, transedges, fratedges)
# @memorized(['orig', 'step'])
def truncated_tf_augmentation(orig, g, trans, frat, col, nodes,
                              step, td, ldoFunc):
    fratGraph = Graph()
    newTrans = {}
    print "Ready to go"

    for v in g:
        for x, y, _ in g.trans_trips_weight(v, step):
            newTrans[(x, y)] = step
            # assert (not g.adjacent(x, y)), "{0} {1} transitive but
            # adjacent".format(x, y)
        for x, y, _ in g.frat_trips_weight(v, step):
            fratGraph.add_edge(x, y)
            # assert (not g.adjacent(x, y)), "{0} {1} fraternal but
            # adjacent".format(x, y, list(g.arcs))
    print "Finished adding to newTrans"

    for (s, t) in newTrans:
        g.add_arc(s, t, step)
        fratGraph.remove_edge(s, t)
    print "Finished removing from fratGraph and adding to g"

    indegs = []
    for v in g:
        #Flexible  indegs[v] = g.in_degree(v)
        if v < len(indegs):
            indegs[v] = g.in_degree(v)
        else:
            indegs.extend([0 for x in range(len(indegs), v)])
            indegs.insert( v, g.in_degree(v) )
    print "Finished initializing indegs"

    fratDigraph = ldoFunc(fratGraph, indegs)
    print "Finished ldo"

    # calculate result
    trans.update(newTrans)
    print "Finished updating"

    for s, t, _ in fratDigraph.arcs():
        frat[(s, t)] = step
        g.add_arc(s, t, step)
    print "Finished adding to g"

    print sys.getsizeof(trans), sys.getsizeof(frat)
    print sys.getsizeof(g)
    g.get_size()

    return (g, trans, frat)
# end def
