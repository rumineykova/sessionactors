__author__ = 'rn710'
from cell.actors import Actor
from cell.roles import role, protocol, protocol_system_start, ProtocolMailbox

cc, CounterProtocol, C, P = "cc", "CountProtocol", "C", "P"

@protocol(cc, CounterProtocol, C, P)
class Counter(Actor):
    class state(Actor.state):
        @role(cc)
        def join(self, cc, cid):
            self.current = 0
            return True

        @role(cc, P)
        def val(self, c, n):
            self.current+=n

        @role(cc, P)
        def retrieve_message(self, cc):
            cc.P.call.res(n = self.current)


@protocol(cc, CounterProtocol, P, C)
class Producer(Actor):
    class state(Actor.state):
        @role(cc)
        def join(self, cc, cid):
            return True

        @role(cc)
        def init(self, cc, n):
             for i in range(1, n):
                cc.C.call.val(n = 1)
             cc.C.call.retrieve_message()

        @role(cc, C)
        def res(self, cc, n):
            print 'The result is', n

def start_protocol():
    # On ActorSystem config
    protocol_system_start(CounterProtocol)
    # Start the protocol
    (prot, _) = ProtocolMailbox.create(CounterProtocol, [P])
    # Initiate the first action
    prot[P].call.init(n = 10)

def start_protocol_old():
    from kombu import Connection
    from cell.agents import dAgent
    from cell.examples import barber
    from cell.examples.count import Producer, Counter
    agent = dAgent(Connection())
    producer = agent.spawn(Producer)
    consumer = agent.spawn(Counter)
    import time
    time.sleep(5)
    consumer.call.join().result()
    producer.call.join(n = 10)