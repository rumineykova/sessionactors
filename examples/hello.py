from kombu.common import uuid
from cell.actors import Actor, ActorProxy
from cell.agents import dAgent
from kombu.connection import Connection
from cell.roles import role, protocol

c, buyer_prot, buyer, seller = 'c', 'buyer_prot', 'buyer', 'seller'

@protocol(c, buyer_prot, seller, [buyer])
class GreetingActor(Actor):
    class state(Actor.state):
        @role(c, buyer)
        def greet(self, who='world'):
            print 'the instance of c.buyer is', c.buyer
            #c.buyer.send('bye')
            print 'Hello', who

@protocol(c, buyer_prot, buyer, [seller])
class ByeActor(Actor):
    class state(Actor.state):
        def bye(self, who='world'):
            print 'Bye %s' % who

#Run from the command line:
"""
from kombu import Connection
from examples.hello import GreetingActor
from cell.agents import dAgent


agent = dAgent(Connection())
greeter = agent.spawn(GreetingActor)
greeter.call('greet')
greeter = agent.select(GreetingActor)
from examples.workflow import Printer
id = agent.select(Printer)
"""


if __name__=='__main__':
    """agent = dAgent(Connection())
    actor = agent.spawn(GreetingActor)

    actor.send.greet({'who':'hello'})
    actor.send.greet({'who':'hello'})
    first_reply(actor.scatter.greet({'who':'hello'}))
    """