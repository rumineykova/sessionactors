__author__ = 'rn710'

from cell.actors import Actor
from cell.roles import role, protocol, protocol_system_start, ProtocolMailbox
from cell.configuration import get_group_id
c, c1, buyer_prot, buyer, seller, seller1, buyer1, n = \
    'c','c1', 'Example', 'buyer', 'seller', 'seller1','buyer1', 'n'


@protocol(c, buyer_prot, seller, [buyer])
class Ping(Actor):
    class state(Actor.state):
        @role(c, buyer)
        def sell(self, c):
            print 'Sell world!'
            print 'the role instance is c:', c
            #print 'the parameter is', p
            print 'I am sending to:', c.buyer
            print 'I am sending to id', c.buyer.id
            print 'I am sending to:', c.buyer.call.buy(p='hello')

        @role(c)
        def join(self, c, cid):
            print 'Ping joined with cid=', cid

    def func(self):
        return self.state.sell()

@protocol(c, buyer_prot, buyer, [seller])
class Pong(Actor):
    class state(Actor.state):
        @role(c)
        def buy(self, c, p):
            print 'Buy the world!'
            print 'the parameter is', p
            print 'buyer1 of c1 is ', c.seller
            return p

        @role(c)
        def join(self, c, cid):
            print 'Pong joined with cid=', cid

    def func(self, p):
        return self.state.buy(p=p)

@protocol(c, buyer_prot, seller1, [buyer])
class Multi(Actor):
    class state(Actor.state):
        @role(c)
        def buy(self, c, p):
            print 'I am in Multi!'
            print 'the parameter is', p
            print 'seller 1 is', c.seller
            return p

        @role(c)
        def join(self, c, cid):
            print 'Multi joined with cid=', cid

    def func(self, p):
        return self.state.buy(p=p)



# c = Protocol.create("This prot", {role:kwargs})
# self.cid = cid
# c.P.start()

def start_protocol():
    # On ActorSystem config
    protocol_system_start(buyer_prot)
    # Start the protocol
    prot = ProtocolMailbox.create(buyer_prot, [seller])
    # Initiate the first action
    prot[seller].call.sell()

    # Create this particular protocol

    # proxy = ActorProxy(ProtocolMailbox, id=buyer_prot, agent = agent, connection = conn)
    #pr.cast('join', {'cid':cid}, exchange = exprot)

    #e1 = agent.spawn(Pong, None, {'name':cid})
    #e = agent.spawn(Ping, None, {'name':cid})

    #e = ActorProxy(Ping, id='seller', agent = agent, connection = conn, name = cid)

    #e1.add_binding(protocol, routing_key = seller)
    #import time
    #time.sleep(5)
    #e.add_binding(protocol, routing_key = seller)

    # when invoking protocol.create()
    #conn1 = Connection()
    #import uuid
    #cid = "1234"
    #from cell.actors import ActorProxy
    #protocol_mailbox = Exchange(cid, type='direct', auto_delete=True)
    #protocol_mailbox.bind(conn1.channel())
    #e.add_binding(protocol_mailbox, routing_key = seller)

    #conn2 = Connection()
    #proxy = ActorProxy(Multi, id=cid, agent = agent, connection = conn2)
    #proxy.call.join(cid=cid)
    # should return c so we start with whatever function we want

    #import time
    #time.sleep(15)
    #print 'Done'