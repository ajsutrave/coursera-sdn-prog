'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.util import irange
from mininet.log import setLogLevel
from math import floor

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        layers = ['c', 'a', 'e', 'h']
        linkopts_list = [linkopts1, linkopts2, linkopts3]
        
        nodes = []
        for layer_num in xrange(len(layers)):
            layer = layers[layer_num]
            for i in irange(1, fanout**layer_num):
                label = '%s%d' % (layer, i)

                new_node = None
                if layer == 'h':
                    new_node = self.addHost(label)
                else:
                    new_node = self.addSwitch(label)
                nodes.append(new_node)

                if layer !='c':
                    parent = nodes[int(floor((len(nodes)-2) / fanout))]
                    linkopts = linkopts_list[layer_num - 1]
                    self.addLink(new_node, parent, **linkopts)
                    
            

topos = { 'custom': ( lambda: CustomTopo() ) }

if __name__ == '__main__':
    setLogLevel('info')
    ct = CustomTopo(None, None, None)
