---
layout: post
title:  "Maximum Flow"
date:   2019-04-23 16:46:40 +0500
categories: algorithms
mathjax: true
---

> This is a draft. Contains lots of mistakes. Stop here and close the tab. No kidding.

## Maximum-flow problem and the Ford-Fulkerson algorithm

### Flow and flow networks

__flow network__ is a graph $G = (V, E)$ with the following features:
* each edge has a nonnegative capacity - $c_e$
* the is a single node considered as _source_ of the flow
* the is a single node considered as _sink_ that absorbs the flow.
* no edge enters the _source_ and no edges leaves _sink_
* there is at least one edge incident to each node.

the nodes other than _source_ and _sink_ are called _internal_ nodes.

__flow__ is a function $f$ that maps each edge _e_ to a nonnegative real number: $f: e \to r$; the value of $f(e)$ represents the amount of flow carried by edge $e$. a flow $f$ must satisfy the following two properties:
1. __capacity conditions__: for each $e \in e$, we have $ 0<= f(e) <= c_e$. the flow on edge $e$ cannot exceed the capacity of edge. i.e: flow in equals flow out.

2. __conservation conditions__: for each nodes $v$ other than $s$ and $t$, we have $ \sum_{v \in v} f(v, u) = \sum_{v \in v} f(u, v) $. The node $v$ can omit as much flow as incoming from $u$.

The flow from $u$ to $v$ is a nonnegative and defined as $f(u, v)$.

The value of a flow $f$ is denoted with $\vert f \vert$ and defined as: $\vert f \vert = \sum_{v \in v} f(s, v) - \sum_{v \in v} f(v, s)$.

That is, the total from out of source to adjacent vertexes minus the total flow from adjacent vertexes into source. yes, this can happen, where source node has both incoming and outgoing edges.

Even if we have a rule "no edge enters the _source_". But, this formula covers only "residual networks".

to solve this problem we use ford-fulkerson method. this method iteratively increases the value of the flow.

todo: write about this method.

### residual networks

the residual network consists of edges with capacities that represent how we can change the flow on edge of graph g. the residual network is denoted as $g_f$. some edges of the flow network does not use all the capacity of the edge. so, it can admit more flow: capacity minus flow. we place that edge into $g_f$ with "residual capacity" of $c_f(u,v) = c(u,v) - f(u,v)$. those edges whose flow equals their capacity are not included in $g_f$. however, the residual network can contain edges that does not exist in original graph. more formally, the **residual capacity** defined as follows:
$$c_f(u, v) = \begin{cases} c(u, v) - f(u, v) & \text{if (u, v) $\in$ e} \\
                            f(u, v) & \text{if(v, u) $\in$ e} \\
                            0 & \text{otherwise}
              \end{cases}$$

we choose a path from residual network and then augment that path with flow $f$. the augmented flow is denoted as $f \arrow_up f$ and its definition is previous flow plus the new flow minus going back flow. we find the minimum flow in the residual path and send it to the path. this avoid getting going back flows. the intuition behind this  definition as follows:

> we increase the flow on .u; 􏰁/ by f 0.u; 􏰁/ but decrease it by f 0.􏰁; u/ because pushing flow on the reverse edge in the residual network signifies decreasing the flow in the original network. pushing flow on the reverse edge in the residual network is also known as cancellation. for example, if we send 5 crates of hockey pucks from u to 􏰁 and send 2 crates from 􏰁 to u, we could equivalently (from the perspective of the final result) just send 3 creates from u to 􏰁 and none from 􏰁 to u. cancellation of this type is crucial for any maximum-flow algorithm

the path from $s$ to $t$ in the residual network is called __augmenting path__. we can increase the flow of edge $(u, v)$ of an aughmenting path by up to $c_f(u, v)$. the maximum amount by which we can increase the flow of edges in the path is called a __residual capacity__ and it is defined as: $c_f(p) = \min\{ c_f(u, v): (u, v) \text{ is on } p \}$

lemma 26.1
letgd.v;e/beaflownetworkwithsourcesandsinkt,andletf beaflow ing. letgf betheresidualnetworkofginducedbyf,andletf0 beaflow in gf . then the function f " f 0 defined in equation (26.4) is a flow in g with valuejf "f0jdjfjcjf0j.


### cuts of flow networks

we get a maximum flow continously augmenting the flow along augmenting paths until there are no paths left from $s$ to $t$. the problem is how do we verify the maximum flow. we need techniques for bounding the size of maxflow. the basic idea is to find a __bottleneck__ for the flow and all flow needs to cross the bottleneck.
a minimum cut of a network is a cut whose capacity is minimum over all cuts of the network. 

the max-flow min-cut theorem tells us that a flow is maximum if and only if its residual network contains no augmenting path.

firstly, a cut $(s, t)$ of flow $g = (v, e)$ is partition of $v$ into $s$ and $t = v - s$. simply, the first half of the cut contains all the sources of $g$. the net-flow $f(s,t)$ is defined as $$f(s,t) = \sum_{u \in s} \sum_{v \in t} f(u, v) - \sum_{u \in s} \sum_{v \in t} f(v, u)$$ 

that is the sum of flow going to cut $s$ minus sum of flows going back from $t$ into $s$.

the capacity of cut is $c(s, t) = \sum_{u \in s} \sum_{v \in t} c(u, v)$

the __minimum cut__ of network is a cut whose capacity in minimum over all cuts of the network.



```python

```
