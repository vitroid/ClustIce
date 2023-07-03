import itertools as it

import networkx as nx
import numpy as np
from sklearn import manifold


def constellation(g, edgelen=1.0, max_iter=1000):
    """
    A rough estimate of the positions of the nodes

    k: bond length
    """
    # Prepare the distance matrix
    D = dict(nx.all_pairs_shortest_path_length(g))
    nnode = len(g.nodes)
    table = np.zeros([nnode, nnode])
    for i in D:
        for j, d in D[i].items():
            table[i,j] = d * edgelen
            table[j,i] = d * edgelen

    # Find the constellation that satisfies the distances.
    mds = manifold.MDS(n_components=3,
                    dissimilarity="precomputed",
                    max_iter=max_iter,
                    n_init=100,
                    metric=True)
    pos = mds.fit_transform(table)

    # layout = {i:v for i, v in enumerate(pos)}
    return pos


#################################################
# spring_layout modified from graphform
# https://github.com/vitroid/GraphForm
class Interaction:
    def __init__(self, forcefunc):
        self.func = forcefunc

    def force(self, vertex0, vertex1):
        d = vertex0.position - vertex1.position
        r = np.linalg.norm(d)
        f = self.func(r) * d / r
        vertex0.force += f
        vertex1.force -= f


class Vertex():
    """
    A vertex is a point mass.
    """
    def __init__(self, pos=None):
        if pos is None:
            self.position = np.random.random(3) * 3
        else:
            self.position = pos
        self.velocity = np.zeros(3)
        self.force = np.zeros(3)

    def force2vel(self):
        self.velocity = self.force + 0

    def progress(self, deltatime):
        self.position += self.velocity * deltatime

    def resetf(self):
        self.force = np.zeros(3)


def radius(vertices):
    """
    Radius of gyration
    """
    pos = np.array([vx.position for key, vx in vertices.items()])
    return np.sum(pos*pos) / pos.shape[0]


def relax(vertices, g, edgelen):
    """
    move vertices to reduce the energy

    interaction is a function of a vector.

    R0: equilibrium length of an edge.
    """
    K = 1
    KR = 1
    # distance of a skip pair.
    golden = 1.62
    skiplen = edgelen * golden
    attractive = Interaction(lambda r: -K * (r - edgelen))
    attractive2 = Interaction(lambda r: -K * (r - skiplen) / 2)
    # repulsive = Interaction(lambda r: repel(r, KR, Rrep))

    # reset the force at vertices.
    for v in vertices:
        vertices[v].resetf()

    # accumulate force

    # bond length
    for i, j in g.edges():
        attractive.force(vertices[i], vertices[j])
    # containing angle
    for i in g:
        for j,k in it.combinations(g.neighbors(i), 2):
            attractive2.force(vertices[j], vertices[k])

    # damped action
    for v in vertices:
        vertices[v].force2vel()
        vertices[v].progress(0.3)
    # Centering
    com = np.mean(np.array([vertices[v].position for v in g]), axis=0)
    for v in g:
        vertices[v].position -= com


def tune_layout(g0, layout, edgelen=1.0, max_iter=100):
    """
    Optimize the positions of the nodes in g0 and embed them as attributes.

    layout:   array of positions
    k:        Bond length.
    max_iter: Number of iterations in the optimization.
    """

    # force g be an undirected graph
    g = nx.Graph(g0)
    vertices = dict()
    for v in g:
        vertices[v] = Vertex(pos=layout[v])
    verbose = 1
    for i in range(max_iter):
        relax(vertices, g, edgelen)
        if i+1 == verbose:
            print(verbose, radius(vertices))
            verbose *= 2

    new_layout = np.zeros_like(layout)
    # update the positions in g0
    for key, vx in vertices.items():
        new_layout[key] = vx.position

    return new_layout