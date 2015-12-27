from cell.actors import Actor
from cell.roles import role, protocol

#my_app = celery.Celery(broker='pyamqp://guest@localhost//')
#agent = dAgent(connection=my_app.broker_connection())
c, Big, A, B, S = 'c', 'Big', 'A', 'B', 'S'

@protocol(c, Big, B, [A, S])
class Pong(Actor):	
    class state(Actor.state):
        @role(c)
        def join(self, c):
            c.A.call.ping()

        @role(c, A)
        def ping(self, c):
            c.A.call.pong()

        @role(c, A)
        def pong(self, c):
            c.S.call.done()

        @role(c, S)
        def done(self, c):
            print 'Pong is done.'

@protocol(c, Big, A, [B, S])
class Ping(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c):
            c.B.call.ping()

        @role(c, B)
        def ping(self, c):
            c.B.call.pong()

        @role(c, B)
        def pong(self, c):
            c.S.call.done()

        @role(c, S)
        def done(self, c):
            print 'Ping is done'

@protocol(c, Big, S, [A, B])
class Sink(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, n):
            print 'In join'
            self.n = n
            return True

        @role(c)
        def done(self, c):
            print 'In done and n is', self.n
            if self.n <=1:
                c.A.call.done()
                c.B.call.done()
                print "The sink is done"
            else: self.n=self.n-1

def start_protocol():
    from kombu import Connection
    from cell.agents import dAgent
    from cell.examples import big
    from cell.examples.big import Ping, Pong, Sink
    agent = dAgent(Connection())
    sink = agent.spawn(Sink)
    ping = agent.spawn(Ping)
    pong = agent.spawn(Pong)
    import time
    time.sleep(2)
    s = sink.call.join(n=2)
    s.result()
    ping.call.join()
    pong.call.join()