from cell.actors import Actor
from roles import role, protocol

#my_app = celery.Celery(broker='pyamqp://guest@localhost//')
#agent = dAgent(connection=my_app.broker_connection())
c1, PCBounded, B, P, C = "c1", "PCBounded", "B", "P", "C"


@protocol(c1, PCBounded, B, [P, C])
class Buffer(Actor):
    class state(Actor.state):
        def join(self, c):
            c1.P.call.produce()

        @role(c1, P)
        def dm(self, c1, data):
            c1.P.call.produce()
            c1.C.call.dm(data)

        @role(c1, P)
        def exit(self, c1):
            print 'I am done'
	
@protocol(c1, PCBounded, P, [C, B])
class Producer(Actor):
    class state(Actor.state):
        def join(self, data):
            self.data = data
            return True

        @role(c1, B)
        def produce(self, c1):
            if not self.data:
                c1.B.call.exit()
            else:
                c1.B.call.dm('foo')

@protocol(c1, PCBounded, C, [B, P])
class Consumer(Actor):
    class state(Actor.state):
        @role(c1, B)
        def dm(self, c1, data):
            print 'The data is:', data
            c1.B.call.more()

def start_protocol():
    from kombu import Connection
    from cell.agents import dAgent
    from cell.examples import big
    from cell.examples.pcbounded import Producer, Consumer, Buffer
    agent = dAgent(Connection())
    producer = agent.spawn(Producer)
    consumer = agent.spawn(Consumer)
    buffer = agent.spawn(Buffer)
    import time
    time.sleep(2)
    producer.call.join(data='foo').result()