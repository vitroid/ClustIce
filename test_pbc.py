from logging import DEBUG, INFO, basicConfig, getLogger

import networkx as nx
from genice2.genice import GenIce
from genice2.plugin import Format, Lattice

from clustice.gromacs import render
from clustice.topology import ice_graph
from clustice.water import tip4p

logger = getLogger()
basicConfig(level=DEBUG)

lattice = Lattice("1h")
formatter = Format("raw", stage=(1, 2))
raw = GenIce(lattice, signature="Ice Ih", rep=(3, 3, 3)).generate_ice(
    formatter
)

# graph is the topology of the hydrogen-bond network
g = nx.Graph(raw["graph"])
# reppositions contains the positions of CoM of water in fractional coordinate
layout = raw["reppositions"]
# repcell is the cell matrix (transposed)
cell = raw["repcell"]

# set orientations of the hydrogen bonds.
dg = ice_graph(g, pos=layout, pbc=True)

# put water molecules
gro = render(
    dg,
    layout @ cell,
    watermodel=tip4p,
    cell=f"{cell[0,0]} {cell[1,1]} {cell[2,2]}",
)
with open(f"save.gro", "w") as f:
    f.write(gro)