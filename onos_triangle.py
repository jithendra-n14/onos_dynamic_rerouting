#!/usr/bin/env python3
"""
onos_triangle.py
----------------
Creates a simple 3-switch triangle topology for ONOS demo.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class TriangleTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add links (triangle)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)

        # Host connections
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)

def run():
    topo = TriangleTopo()
    net = Mininet(topo=topo, controller=None)
    controller = RemoteController('c0', ip='127.0.0.1', port=6653)
    net.addController(controller)
    net.start()

    info("*** Testing network connectivity\n")
    net.pingAll()

    info("*** Starting CLI\n")
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    run()
