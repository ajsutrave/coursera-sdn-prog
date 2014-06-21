'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
        self._firewall_priority = 1

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''

        with open(policyFile) as fp:
            keys = fp.readline().strip().split(',')
            mac_0_idx = keys.index('mac_0')
            mac_1_idx = keys.index('mac_1')
            for line in fp.readlines():
                rule_data = line.strip().split(',')

                msg = of.ofp_flow_mod()
                msg.priority = self._firewall_priority
                msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))
                msg.match.dl_src = EthAddr(rule_data[mac_0_idx])
                msg.match.dl_dst = EthAddr(rule_data[mac_1_idx])
                event.connection.send(msg)


    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
