Maximum-flow problem
=====================

:date: 2019-04-23 16:46:40

:blankline:

    This is a draft. Contains lots of mistakes. Stop here and close the
    tab. No kidding.

Flow and flow networks
~~~~~~~~~~~~~~~~~~~~~~

**Flow network** is a graph :math:`G = (V, E)` with the following
features:

* Each edge has a nonnegative capacity - :math:`c_e`
* There is a single node considered as *source* of the flow
* The is a single node considered as *sink* that absorbs the flow.
* No edge enters the *source* and no edges leaves *sink*
* There is at least one edge incident to each node.

The nodes other than *source* and *sink* are called *internal* nodes.

**Flow** is a function :math:`f` that maps each edge :math:`e` to a
nonnegative real number: :math:`f: e \to r`; the value of :math:`f(e)`
represents the amount of flow carried by edge :math:`e`. a flow
:math:`f` must satisfy the following two properties:


The flow from :math:`u` to :math:`v` is a nonnegative and defined as
:math:`f(u, v)` and value of a flow :math:`f` is denoted with
:math:`\vert f \vert` and defined as:
:math:`\vert f \vert = \sum_{v \in v} f(s, v) - \sum_{v \in v} f(v, s)`.
That is, the total from out of source to adjacent vertexes minus the
total flow from adjacent vertexes into source. yes, this can happen,
where source node has both incoming and outgoing edges.

Even if we have a rule "no edge enters the *source*". But, this formula
covers only "residual networks".

To solve this problem we use Ford-Fulkerson method. This method
iteratively increases overall value of flow and on each iteration
increases the flow of the edges of some path from :math:`s` to :math:`t`
as much as possible:

::

    function ford-fulkerson(G, s, t):
        let flow be 0
        let G_f be the residual network of G
        
        while there exists a path P in Gf:
            let min_res_cap be the minimum residual capacity in P
            augment edges of P by min_res_cap
            increment flow by min_res_cap
        end
        
        return flow
    end

Residual networks
~~~~~~~~~~~~~~~~~

The residual network consists of edges with capacities that represent
how we can change the flow on edge of graph g. the residual network is
denoted as :math:`g_f`. Some edges of the flow network does not use all
the capacity of the edge. So, it can admit more flow: capacity minus
flow. We place that edge into :math:`g_f` with "residual capacity" of
:math:`c_f(u,v) = c(u,v) - f(u,v)`. those edges whose flow equals their
capacity are not included in :math:`g_f`. however, the residual network
can contain edges that does not exist in original graph. more formally,
the **residual capacity** defined as follows:


.. math::

  c_f(u, v) = 
  \begin{cases}
  c(u, v) - f(u, v), & \text{if (u, v) $\in$ e} \\
  f(u, v), & \text{if(v, u) $\in$ e} \ 0 & \text{otherwise}
  \end{cases}


we choose a path from residual network and then augment that path with
flow :math:`f`. the augmented flow is denoted as :math:`f \uparrow f`
and its definition is previous flow plus the new flow minus going back
flow. we find the minimum flow in the residual path and send it to the
path. this avoid getting going back flows. the intuition behind this
definition as follows:

    We increase the flow on :math:`(u, v)` by :math:`f'(u, v)` but
    decrease it by :math:`f'(v, u)` because pushing flow on the reverse
    edge in the residual network signifies decreasing the flow in the
    original network. pushing flow on the reverse edge in the residual
    network is also known as cancellation. for example, if we send 5
    crates of hockey pucks from :math:`u` to :math:`v` and send 2 crates
    from :math:`v` to :math:`u`, we could equivalently (from the
    perspective of the final result) just send 3 creates from :math:`u`
    to :math:`v` and none from :math:`v` to :math:`u`. Cancellation of
    this type is crucial for any maximum-flow algorithm

The path from :math:`s` to :math:`t` in the residual network is called
**augmenting path**. we can increase the flow of edge :math:`(u, v)` of
an aughmenting path by up to :math:`c_f(u, v)`. the maximum amount by
which we can increase the flow of edges in the path is called a
**residual capacity** and it is defined as:
:math:`c_f(p) = \min\{ c_f(u, v): (u, v) \text{ is on } p \}`

**Lemma:** Let :math:`G = (V, E)` be a flow network with source
:math:`s` and sink :math:`t`,and let :math:`f` be a flow in :math:`G`.
Let :math:`G_f` be the residual network of :math:`G` induced by
:math:`f`,and let :math:`f'` be a flow in :math:`G_f`. Then the function
:math:`f \uparrow f'` defined in equation (26.4) is a flow in :math:`G`
with value
:math:`\vert f \uparrow f' \vert = \vert f \vert + \vert f \vert + \vert f' \vert`.

This lemma is true, don't ask me why. Look at CLRS for the proof.

Cuts of flow networks
~~~~~~~~~~~~~~~~~~~~~

we get a maximum flow continously augmenting the flow along augmenting
paths until there are no paths left from :math:`s` to :math:`t`. the
problem is how do we verify the maximum flow. we need techniques for
bounding the size of maxflow. the basic idea is to find a **bottleneck**
for the flow and all flow needs to cross the bottleneck. a minimum cut
of a network is a cut whose capacity is minimum over all cuts of the
network.

the max-flow min-cut theorem tells us that a flow is maximum if and only
if its residual network contains no augmenting path.

firstly, a cut :math:`(s, t)` of flow :math:`g = (v, e)` is partition of
:math:`v` into :math:`s` and :math:`t = v - s`. simply, the first half
of the cut contains all the sources of :math:`g`. the net-flow
:math:`f(s,t)` is defined as

.. math:: f(s,t) = \sum_{u \in s} \sum_{v \in t} f(u, v) - \sum_{u \in s} \sum_{v \in t} f(v, u)

That is the sum of flow going to cut :math:`s` minus sum of flows going
back from :math:`t` into :math:`s`.

The capacity of cut is
:math:`c(s, t) = \sum_{u \in s} \sum_{v \in t} c(u, v)`. The **minimum
cut** of network is a cut whose capacity in minimum over all cuts of the
network.

Code
~~~~

The implementation of this algorithm is written in C++

.. code:: C++

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


<TBA>Analysis of Ford-Fulkerson algorithm</TBA>

<TBA>Better aproach with Edmonds-Karp algorithm</TBA>

