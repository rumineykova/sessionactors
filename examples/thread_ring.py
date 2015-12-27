__author__ = 'rn710'
from cell.actors import Actor
from cell.roles import role, protocol
from cell.configuration import prot_config, get_group_id

#my_app = celery.Celery(broker='pyamqp://guest@localhost//')
#agent = dAgent(connection=my_app.broker_connection())
c, ThreadRing, W, n = "c", "ThreadRing", "W", 'n'

@protocol(c, ThreadRing, W, [W], {W:n}, True)
class Workers(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c, num):
            self.num = num
            self.done = False
            return True

        @role(c, W)
        def data(self, c, data):
            if self.done:
                print 'We are done'
            else:
                self.done = True
                print 'the data I am receving is', data
                c.W[self.num+1 / ThreadRingConfig.numWorkers].call.data(data=data)

class ThreadRingConfig:
    numWorkers = prot_config[ThreadRing][n]


def start_protocol():
    from kombu import Connection
    from cell.agents import dAgent
    from cell.examples import thread_ring
    from cell.examples.thread_ring import Workers
    agent = dAgent(Connection())
    import time
    time.sleep(3)
    worker = agent.spawn(Workers, id = get_group_id(W, 1))
    worker.call.join(num = 1).result()
    for i in range(2, ThreadRingConfig.numWorkers):
        worker = agent.spawn(Workers, id = get_group_id(W, i))
        time.sleep(3)
        worker.call.join(num = i).result()
    time.sleep(3)
    worker.call.data(data='hello world!')