Contraction Hierarchies
=======================

:date: 2019-02-27 16:46:40


Genius algorithm to find shortest paths in a large graph. The algorithms
consists from 2 stages:

1) Preporessing stage that create indices
2) Query stage that uses indices to find a shortest path.

Preprocess
----------

The goal is to develop an alternate Dijkstra's algorithm that can ignore some node :math:`v` and stops when given max distance is reached.

We use this algorithm to find shortcuts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1) Start from choosing a random node.
2) Calculate the max distance between incident nodes:

   - When contracting node :math:`v`, we need to insert the shortcut :math:`u \to w`, if and only if :math:`u \to v \in E` and :math:`v \to w \in E` and :math:`u \to v \to w` is the only shortest path from :math:`u` to :math:`w`.
   - When contracting node :math:`v`, for any pair of edges :math:`(u, v)` and :math:`(v, w)` we want to check whether there is a witness path from u to :math:`w` bypassing :math:`v` with length at most :math:`l(u,v)+l(v,w)` — then there is no need to add a shortcut from :math:`u` to :math:`w`.

3) Make 1 hop backward search for each predecessor of target node v
4) Last node does not need to be contracted
5) Compute the importance for the top node on the priority queue, then
   compare it with the other top node, if its importance is less, then
   put the node back into the queue.
6) Already contracted nodes can be distinguished by their ranks: already
   contracted nodes have lower rank than currently contracting node. So,
   instead of having an array for contracted nodes, use the rank array.
   Motherfucker!
7) Stop limits can be various:

   - max\_incoming + max\_outgoing
   - cost(v, x) + max\_outgoing - min\_outgoing
   - cost(v, x) + max\_outgoing - min(x, w)

Node ordering
~~~~~~~~~~~~~

It is important because query time and preprocessing heavily depends on
it. Nodes must be measure my some importance criterias and the least
important nodes must be contracted first. Further, several importance
criterias will be covered:

Edge difference
^^^^^^^^^^^^^^^

-  Want to minimize the number of edges in the augmented graph
-  Number of shortcuts have to be added if node v is contracted s(v),
   incoming degree in(v) and outgoing degree out(v)
-  Lets suppose that there are 3 incoding endges and 5 outgoing edges,
   what is the worst case count of shortcuts if we contract this node ?
-  It is in(v) \* out(v)
-  Edge difference ed = s(v) - in(v) - out(v)
-  Number of edges increases by ed after contracting v
-  Contract node with small edge difference

Number of contracted neighbors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Want to spread contracted nodes across the graph
-  Contract a node with small number of already contracted neighbors
   cn(v)

Shortcut Cover
^^^^^^^^^^^^^^

-  Want to contract important nodes late
-  Shortcut cover sc(v) - the number of neighbors w of v such that we
   have to shortcut to or from w after contracting v.
-  If shortcut cover is big, many nodes depend on v
-  Contract a node with small sc(v)

Node level (?)
^^^^^^^^^^^^^^

-  Node level L(v) is an upper bound on the number of edges in the
   shortest path from any s to v in the augmented graph
-  Initially, L(v) = 0
-  After contracting node v, for neighbors u of v do L(u) = max(L(u),
   L(v) + 1)

-  Contract a node with small L(v)

Query
-----

TBA

Code
----

.. code:: python

    import queue
    import sys
    import time


    INF = sys.maxsize


    class ContractionHierarchies:
        def __init__(self, n, m, g, g_r, costs, costs_r):
            self.n = n
            self.m = m
            self.g = g
            self.g_r = g_r
            self.costs = costs
            self.costs_r = costs_r
            self.node_level = [0] * n
            self.max_outgoing = [max(w) if len(w) else 1 for w in costs]
            self.min_outgoing = [min(w) if len(w) else INF for w in costs_r]
            self.rank = [INF] * n

        def witness_search(self, s, v, max_dist):
            dist = dict()
            dist[s] = 0

            heap = queue.PriorityQueue()
            heap.put((0, s))
            max_hops = 3
            hops = 0

            while not heap.empty() and hops < max_hops:
                hops += 1
                d, u = heap.get()

                if max_dist <= d:
                    break

                for x, w in self.g[u]:
                    if self.rank[x] < self.rank[v] or x == v:
                        continue

                    if d + w < dist.get(x, INF):
                        dist[x] = d + w
                        heap.put((dist[x], x))

            return dist

        def contract(self, v, adding_shortcuts=False):
            shortcuts = list()
            shortcuts_cover = set()
            shortcut_count = 0
            delta = self.max_outgoing[v] - self.min_outgoing[v]

            for u, u_d in self.g_r[v]:
                if self.rank[u] < self.rank[v]:
                    continue

                limit = u_d + delta
                dist = self.witness_search(u, v, limit)

                for w, _ in self.g[v]:
                    if self.rank[w] < self.rank[v]:
                        continue

                    add_shortcut = True

                    for x, d in self.g_r[w]:
                        if self.rank[x] < self.rank[v] or x == v:
                            continue

                        cost = dist.get(x, INF)

                        if self.costs_r[v][u] + self.costs[v][w] >= cost + d:
                            add_shortcut = False
                            break

                    if add_shortcut:
                        shortcut_count += 1
                        shortcuts_cover.add(u)
                        shortcuts_cover.add(w)

                        if adding_shortcuts:
                            shortcuts.append((u, w, self.costs_r[v][u] + self.costs[v][w]))

            edge_difference = shortcut_count - len(self.g[v]) - len(self.g_r[v])
            return edge_difference + self.compute_node_level(v) + len(shortcuts_cover), shortcuts

        def compute_node_level(self, v):
            n, level = 0, 0

            for u, _ in self.g[v]:
                if self.rank[u] != INF:
                    n += 1
                    level = max(self.node_level[u]+1, level)

            for u, _ in self.g_r[v]:
                if self.rank[u] != INF:
                    n += 1
                    level = max(self.node_level[u]+1, level)

            return n + level/2

        def update_node_level(self, v):
            for u, _ in self.g[v]:
                self.node_level[u] = max(self.node_level[u], self.node_level[v]+1)

            for u, _ in self.g_r[v]:
                self.node_level[u] = max(self.node_level[u], self.node_level[v]+1)

        def add_shortcuts(self, shortcuts):
            for shortcut in shortcuts:
                u, v, w = shortcut
                if self.max_outgoing[u] < w:
                    self.max_outgoing[u] = w

                if w < self.min_outgoing[u]:
                    self.max_outgoing[v] = w

                self.g[u].append((v, w))
                self.g_r[v].append((u, w))

                self.costs[u][v] = w
                self.costs_r[v][u] = w

        def remove_edges(self):
            for i in range(self.n):
                j, k = 0, len(self.g[i])
                while j < k:
                    if self.rank[self.g[i][j][0]] < self.rank[i]:
                        self.costs[i][self.g[i][j][0]] = INF
                        del self.g[i][j]
                        k -= 1
                        continue
                    j += 1

                j, k = 0, len(self.g_r[i])
                while j < k:
                    if self.rank[self.g_r[i][j][0]] < self.rank[i]:
                        self.costs_r[i][self.g_r[i][j][0]] = INF
                        del self.g_r[i][j]
                        k -= 1
                        continue
                    j += 1

        def preprocess(self):
            counter = 0
            rank_count = 0
            pq = queue.PriorityQueue()

            print("n:", self.n)
            for i in range(self.n):
                c, _ = self.contract(i)
                pq.put((c, i))

            while pq.qsize() > 1:
                counter += 1

                _, u = pq.get()
                ved, v = pq.get()

                ed, shortcuts = self.contract(u, adding_shortcuts=True)

                if ed <= ved:
                    self.add_shortcuts(shortcuts)
                    self.rank[u] = rank_count
                    self.update_node_level(u)
                else:
                    pq.put((ed, u))

                rank_count += 1
                pq.put((ved, v))

            print("counter:", counter)
            self.remove_edges()

        def query(self, s, t):
            estimate = INF

            pq = queue.PriorityQueue()
            pq_r = queue.PriorityQueue()

            pq.put((0, s))
            pq_r.put((0, t))

            dist = [INF] * self.n
            dist_r = [INF] * self.n
            dist[s] = 0
            dist_r[t] = 0

            visited = [INF] * self.n
            visited_r = [INF] * self.n

            while not pq.empty() or not pq_r.empty():
                if not pq.empty():
                    _, u = pq.get()

                    if dist[u] <= estimate:
                        for v, w in self.g[u]:
                            if dist[v] > dist[u] + w:
                                dist[v] = dist[u] + w
                                pq.put((dist[v], v))

                    visited[u] = True
                    if visited_r[u] and dist[u] + dist_r[u] < estimate:
                        estimate = dist[u] + dist_r[u]

                if not pq_r.empty():
                    _, u = pq_r.get()

                    if dist_r[u] < estimate:
                        for v, w in self.g_r[u]:
                            if dist_r[v] > dist_r[u] + w:
                                dist_r[v] = dist_r[u] + w
                                pq_r.put((dist[v], v))

                    visited_r[u] = True
                    if visited[u] and dist[u] + dist_r[u] < estimate:
                        estimate = dist[u] + dist_r[u]

            return -1 if estimate == INF else estimate


    def readl():
        return map(int, sys.stdin.readline().split())


    def init():
        n, m = readl()

        g = [[] for _ in range(n)]
        g_r = [[] for _ in range(n)]

        costs = [[0 for _ in range(n)] for _ in range(n)]
        costs_r = [[INF for _ in range(n)] for _ in range(n)]

        for _ in range(m):
            u, v, w = readl()
            costs[u-1][v-1] = w
            costs_r[v-1][u-1] = w

            g[u-1].append((v-1, w))
            g_r[v-1].append((u-1, w))

        return ContractionHierarchies(n, m, g, g_r, costs, costs_r)


    if __name__ == '__main__':
        ch = init()

        start_time = time.time()
        ch.preprocess()
        print("Ready")
        print("preprocessing took %s seconds" % (time.time() - start_time))
        sys.stdout.flush()

        t, = readl()

        for i in range(t):
            s, t = readl()
            start_time = time.time()
            print(ch.query(s-1, t-1))
            print("querying took %s seconds" % (time.time() - start_time))

