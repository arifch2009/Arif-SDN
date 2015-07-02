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
from csv import DictReader


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''

Policy = namedtuple('Policy', ('dl_src', 'dl_dst'))
 


class Firewall (EventMixin):

	def __init__ (self):
        	self.listenTo(core.openflow)
        	log.debug("Enabling Firewall Module")

   	def read_policies (self, file):
        	with open(file, 'r') as f:
            		reader = DictReader(f, delimiter = ",")
            		policies = {}
            		for row in reader:
                		policies[row['id']] = Policy(EthAddr(row['mac_0']), EthAddr(row['mac_1']))
        	return policies

    	def _handle_ConnectionUp (self, event):
        
    		policies=self.read_policies(policyFile)

		for policy in policies.itervalues():
			msg=of.ofp_flow_mod()
			msg.priority=20
			msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))

		# Creating a match
			match=of.ofp_match()
		
		#For Unidirection
			match.dl_src=policy.dl_src
			match.dl_dst=policy.dl_dst
		
			msg.match= match

			event.connection.send(msg)
		
		# For Opposite direction
			match.dl_src=policy.dl_dst
			match.dl_dst=policy.dl_src
			msg.match= match

			event.connection.send(msg)
		
		#debug
            		log.info("Installing firewall rule for src=%s, dst=%s" % (policy.dl_src, policy.dl_dst))
            		log.debug(msg)

	
		
		log.info("Hubifying %s", dpidToStr(event.dpid))	

        	log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
	'''
    	Starting the Firewall module
    	'''
    	core.registerNew(Firewall)
