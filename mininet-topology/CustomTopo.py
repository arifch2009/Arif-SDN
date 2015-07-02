'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
	
	a=[]
        c=[]
        h=[]
        e=[]

        print '**********Adding Code Switches********'
        for i in range(1, fanout+1):
                coreSwitch=self.addSwitch('c%s' % i)
                c.append(coreSwitch)
		break
        print 'Total Core Switches:', len(c)
        print 'Core Switches  are :' , c

        print '**********Adding Aggregation Switches********'
        for i in range(1, fanout+1):
                aggSwitch=self.addSwitch('a%s' % i)
                self.addLink(c[0], aggSwitch, **linkopts1)
                a.append(aggSwitch)
        print 'Total Aggregation Switches:', len(a)
        print 'Aggregation Switches  are :' , a


        print '**********Adding Edge Switches********'
        counter=1
        for j in range(0, len(a)):
                for i in range(1, fanout+1):
                        edgeSwitch=self.addSwitch('e%s' % counter)
                        counter=counter+1
                        self.addLink(a[j], edgeSwitch, **linkopts2)
                        e.append(edgeSwitch)
        print 'Total Edge Switches:', len(e)
        print 'Edge Switches  are :' , e

        print '**********Adding Hosts********'
        counter=1
        for j in range(0, len(e)):
                for i in range(1, fanout+1):
                        host=self.addHost('h%s' % counter)
                        counter=counter+1
                        self.addLink(e[j], host, **linkopts3)
                        h.append(host)
	
	print 'Total Host:', len(h)
        print 'Host  are :' , h        
        '''
	core_switch = self.addSwitch('c1')

	aggr_len = 0
	edge_len = 0
	host_len = 0

	for i in range(fanout):
		aggr_len+=1
		aggr_switch = self.addSwitch('a%d' % aggr_len)
		self.addLink(core_switch, aggr_switch, **linkopts1)
		for j in range(fanout):
                	edge_len+=1
                	edge_switch = self.addSwitch('e%d' % edge_len)
                	self.addLink(aggr_switch, edge_switch, **linkopts2)
			for k in range(fanout):
                        	host_len+=1
                        	host = self.addHost('h%d' % host_len)
                        	self.addLink(edge_switch, host, **linkopts3)

        '''    
topos = { 'custom': ( lambda: CustomTopo() ) }

