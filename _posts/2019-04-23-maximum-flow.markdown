---
layout: post
title:  "Maximum Flow"
date:   2019-04-23 16:46:40 +0500
categories: algorithms
mathjax: true
---

> This is a draft. Contains lots of mistakes. Stop here and close the tab. No kidding.

## Maximum-flow problem with Ford-Fulkerson and Edmonds-Karp algorithms

TODO: improve
This blog post explains hard mathematical proofs of max-flow min cut theorem and digest of my readings on CRLS.

### Flow and flow networks

__Flow network__ is a graph $G = (V, E)$ with the following features:
* Each edge has a nonnegative capacity - $c_e$
* The is a single node considered as _source_ of the flow
* The is a single node considered as _sink_ that absorbs the flow.
* No edge enters the _source_ and no edges leaves _sink_
* There is at least one edge incident to each node.

The nodes other than _source_ and _sink_ are called _internal_ nodes.

__Flow__ is a function $f$ that maps each edge $e$ to a nonnegative real number: $f: e \to r$; the value of $f(e)$ represents the amount of flow carried by edge $e$. a flow $f$ must satisfy the following two properties:

1. __Capacity conditions__ - for each $e \in e$, we have $ 0<= f(e) <= c_e$. the flow on edge $e$ cannot exceed the capacity of edge. i.e: flow in equals flow out.

2. __Conservation conditions__ - for each nodes $v$ other than $s$ and $t$, we have $ \sum_{v \in v} f(v, u) = \sum_{v \in v} f(u, v) $. The node $v$ can omit as much flow as incoming from $u$.

The flow from $u$ to $v$ is a nonnegative and defined as $f(u, v)$ and value of a flow $f$ is denoted with $\vert f \vert$ and defined as: $\vert f \vert = \sum_{v \in v} f(s, v) - \sum_{v \in v} f(v, s)$. That is, the total from out of source to adjacent vertexes minus the total flow from adjacent vertexes into source. yes, this can happen, where source node has both incoming and outgoing edges.

Even if we have a rule "no edge enters the _source_". But, this formula covers only "residual networks".

To solve this problem we use Ford-Fulkerson method. This method iteratively increases overall value of flow and on each iteration increases the flow of the edges of some path from $s$ to $t$ as much as possible:

```
function ford-fulkerson(G, s, t):
    let flow be 0
    let G_f be the residual network of G
    
    while there exists a path P in Gf:
        let min_res_cap be the minimum residual capacity in P
        augment edges of P by min_res_cap
        increment flow by min_res_cap
    end
    
    return flow
```

### Residual networks

The residual network consists of edges with capacities that represent how we can change the flow on edge of graph g. the residual network is denoted as $g_f$. Some edges of the flow network does not use all the capacity of the edge. So, it can admit more flow: capacity minus flow. We place that edge into $g_f$ with "residual capacity" of $c_f(u,v) = c(u,v) - f(u,v)$. those edges whose flow equals their capacity are not included in $g_f$. however, the residual network can contain edges that does not exist in original graph. more formally, the **residual capacity** defined as follows:
$$c_f(u, v) = \begin{cases} c(u, v) - f(u, v) & \text{if (u, v) $\in$ e} \\
                            f(u, v) & \text{if(v, u) $\in$ e} \\
                            0 & \text{otherwise}
              \end{cases}$$

we choose a path from residual network and then augment that path with flow $f$. the augmented flow is denoted as $f \uparrow f$ and its definition is previous flow plus the new flow minus going back flow. we find the minimum flow in the residual path and send it to the path. this avoid getting going back flows. the intuition behind this  definition as follows:

> We increase the flow on $(u, v)$ by $f'(u, v)$ but decrease it by $f'(v, u)$ because pushing flow on the reverse edge in the residual network signifies decreasing the flow in the original network. pushing flow on the reverse edge in the residual network is also known as cancellation. for example, if we send 5 crates of hockey pucks from $u$ to $v$ and send 2 crates from $v$ to $u$, we could equivalently (from the perspective of the final result) just send 3 creates from $u$ to $v$ and none from $v$ to $u$. Cancellation of this type is crucial for any maximum-flow algorithm

The path from $s$ to $t$ in the residual network is called __augmenting path__. we can increase the flow of edge $(u, v)$ of an aughmenting path by up to $c_f(u, v)$. the maximum amount by which we can increase the flow of edges in the path is called a __residual capacity__ and it is defined as: $c_f(p) = \min\{ c_f(u, v): (u, v) \text{ is on } p \}$

**Lemma:** Let $G = (V, E)$ be a flow network with source $s$ and sink $t$,and let $f$ be a flow in $G$. Let $G_f$ be the residual network of $G$ induced by $f$,and let $f'$ be a flow in $G_f$. Then the function $f \uparrow f'$ defined in equation (26.4) is a flow in $G$ with value $\vert f \uparrow f' \vert = \vert f \vert + \vert f \vert + \vert f' \vert$.


### Cuts of flow networks

we get a maximum flow continously augmenting the flow along augmenting paths until there are no paths left from $s$ to $t$. the problem is how do we verify the maximum flow. we need techniques for bounding the size of maxflow. the basic idea is to find a __bottleneck__ for the flow and all flow needs to cross the bottleneck.
a minimum cut of a network is a cut whose capacity is minimum over all cuts of the network. 

the max-flow min-cut theorem tells us that a flow is maximum if and only if its residual network contains no augmenting path.

firstly, a cut $(s, t)$ of flow $g = (v, e)$ is partition of $v$ into $s$ and $t = v - s$. simply, the first half of the cut contains all the sources of $g$. the net-flow $f(s,t)$ is defined as $$f(s,t) = \sum_{u \in s} \sum_{v \in t} f(u, v) - \sum_{u \in s} \sum_{v \in t} f(v, u)$$ That is the sum of flow going to cut $s$ minus sum of flows going back from $t$ into $s$.

The capacity of cut is $c(s, t) = \sum_{u \in s} \sum_{v \in t} c(u, v)$. The __minimum cut__ of network is a cut whose capacity in minimum over all cuts of the network.


### Code

The implementation of this algorithm is written in C++

```C++
#include <algorithm>
#include <iostream>
#include <limits>
#include <stack>
#include <vector>

using std::min;
using std::numeric_limits;
using std::stack;
using std::vector;

struct Edge {
  int from, to, capacity, flow;
};

class FlowGraph {
private:
  vector<Edge> edges;
  vector<vector<size_t>> graph;

public:
  explicit FlowGraph(size_t n) : graph(n) {}

  void add_edge(int from, int to, int capacity) {
    // We first append a forward edge and then a backward edge.
    // All forward edges are stored at EVEN indices (starting from 0),
    // whereas backward edges are stored at ODD indices in the list edges.
    Edge forward_edge = {from, to, capacity, 0};
    Edge backward_edge = {to, from, 0, 0};

    graph[from].push_back(edges.size());
    edges.push_back(forward_edge);

    graph[to].push_back(edges.size());
    edges.push_back(backward_edge);
  }

  size_t size() const { return graph.size(); }

  const vector<size_t> &get_ids(int from) const {
    return graph[from];
  }

  const Edge &get_edge(size_t id) const {
    return edges[id];
  }

  void add_flow(size_t id, int flow) {
    /*
     * To get a backward edge for a true forward edge (i.e id is even), we
     * should get id + 1 due to the described above scheme. On the other hand,
     * when we have to get a "backward" edge for a backward edge (i.e. get a
     * forward edge for backward - id is odd), id - 1 should be taken.
     *
     * It turns out that id ^ 1 works for both cases. Think this through!
     */
    edges[id].flow += flow;
    edges[id ^ 1].flow -= flow;
  }
};

FlowGraph read_data() {
  int vertex_count, edge_count;
  std::cin >> vertex_count >> edge_count;
  FlowGraph graph(vertex_count);
  for (int i = 0; i < edge_count; ++i) {
    int u, v, capacity;
    std::cin >> u >> v >> capacity;
    graph.add_edge(u - 1, v - 1, capacity);
  }
  return graph;
}

vector<int> dfs(FlowGraph &graph, int from, int to) {
  stack<int> s;
  s.push(from);
  vector<bool> used(graph.size());
  vector<int> parent(graph.size(), -1);

  while (!s.empty()) {
    int u = s.top();
    s.pop();
    used[u] = true;

    if(u == to) {
    	break;
    }

    for (auto v : graph.get_ids(u)) {
      const Edge& edge = graph.get_edge(v);
      if ((edge.capacity - edge.flow) <= 0) {
        continue;
      }

      if (!used[edge.to]) {
      	s.push(edge.to);
        parent[edge.to] = v;
      }
    }
  }


  vector<int> path;
  while(to != from) {
    auto id = parent[to];
    if(id == -1) {
      return vector<int>();
    }
    path.push_back(id);
    to = graph.get_edge(id).from;
  }

  return path;
}

int max_flow(FlowGraph &graph, int from, int to) {
  int flow = 0;

  while (true) {
    auto path = dfs(graph, from, to);
    if (path.empty()) {
      break;
    }

    int cf = numeric_limits<int>::max();

    for (auto &edge_id: path) {
      auto edge = graph.get_edge(edge_id);
      cf = min(cf, edge.capacity - edge.flow);
    }

    flow += cf;

    for(auto &edge : path) {
      graph.add_flow(edge, cf);
    }
  }

  return flow;
}

int main() {
  FlowGraph graph = read_data();

  std::cout << max_flow(graph, 0, graph.size() - 1) << "\n";
  return 0;
}

```

### Analysis of Ford-Fulkerson algorithm

### Better aproach with Edmonds-Karp algorithm