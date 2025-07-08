/**
 * @file dot_graphs.h
 *
 * @page dotgraphs Dot Graph Demonstrations
 *
 * @section dotcmd Using \@dot command
 *
 * @dot "basic graph elements"
 * digraph G {
 *     bgcolor="purple:pink" label="a graph" fontcolor="white"
 *     subgraph cluster1 {
 *         fillcolor="blue:cyan" label="a cluster" fontcolor="white" style="filled" gradientangle="270"
 *         node [shape=box fillcolor="red:yellow" style="filled" gradientangle=90]
 *		"a node";
 *    }
 * }
 * @enddot
 *
 * @section dotfilecmd Using \@dotfile command
 *
 * @dotfile "dotfile.dot" "Captions go here"
 */
