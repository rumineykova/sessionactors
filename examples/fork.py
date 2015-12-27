from cell.actors import Actor
from cell.roles import role, protocol, protocol_system_start, ProtocolMailbox
from cell.configuration import get_group_id, prot_config

#my_app = celery.Celery(broker='pyamqp://guest@localhost//')
#agent = dAgent(connection=my_app.broker_connection())
c, KFork, M, W, n = "c", "KFork", "M", "W", 'n'

@protocol(c, KFork, M, [W], {W:n})
class Master(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid = cid)
            return True

        @role(c)
        def init(self, c, n):
            self.n = n
            return True

        @role(c)
        def start(self, c):
            for i in range(1, self.n):
                c.W[i].call.data(data= 'Hello')
                c.W[i].call.end()

@protocol(c, KFork, W, [M, W], {W:n}, True)
class Workers(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, cid):
            self.actor.join(cid = cid)
            return True

        @role(c, M)
        def data(self, c, data):
            print 'data is received:',data

        @role(c, M)
        def end(self, c):
            print "I am done!"

class KForkConfig:
    numWorkers = prot_config[KFork][n]

def start_protocol():
    # On ActorSystem config
    protocol_system_start(KFork)

    # Start the protocol
    prot = ProtocolMailbox.create(KFork, [M])

    # Initiate the first action
    prot[M].call.init(n = KForkConfig.numWorkers)
    prot[M].call.start()


def start_protocol_old():
    from kombu import Connection
    from cell.agents import dAgent
    from cell.examples import fork
    from cell.examples.fork import Workers, Master
    agent = dAgent(Connection())
    import time
    time.sleep(3)
    master = agent.spawn(Master)
    for i in range(1, KForkConfig.numWorkers):
        worker = agent.spawn(Workers, id = get_group_id(W, i))
        time.sleep(3)
        worker.call.join().result()
    time.sleep(3)
    master.call.join(n = KForkConfig.numWorkers).result()
    master.call.start()