__author__ = 'rn710'
import sys
sys.path.append('/homes/rn710/Repositories/spy/MonitorPrototype/src')
#from parsing import base_parser
#from core.fsm import FSM
from cell import examples
from cell.actors import ActorProxy
from cell.actors import Actor
from cell.utils import qualname
from configuration import role_mapping_config as config
from configuration import prot_config, get_group_id, role_mapping_config

#my_app = celery.Celery(broker='pyamqp://guest@localhost//')
#agent = dAgent(connection=my_app.broker_connection())


class ActorRoleProxy(object):
    def __init__(self, name):
        self.name = name

# This is a base class for monitor (used for testing)
# To turn on the monitor the class is replaced by the ConversationMonitor in the configuration
# The path to the protocol files is also given
class Monitor(object):
    def __init__(self):
        pass

    def initialise(self, prot, self_role):
        print 'Initialise an FSM for:'
        # get_prot(prot, self, role)
        # the protocol dir should be configured in the configuration

    def check(self, sender, receiver, label):
        print 'Chech the transition:(sender, receiver, label): %s, %s, %s'\
        %(sender, receiver, label)

class ActorRole(object):
    def __init__(self, cls, prot, self_role, others, group_roles={}):
        self.prot = prot
        self.self_role = self_role
        self.others = others
        # set group roles if any
        self.group_roles = group_roles

        self.monitor = Monitor()
        self.monitor.initialise(prot, self_role)
        if str(qualname(cls)) == '__builtin__.unicode':
            self.cls_name = cls
        else:
            self.cls_name = qualname(cls)
        self.other_set = False

    def subprotocol(self, protocol, roles):
        pass

    def check(self, from_role, func):
        # check the transition (from_role, to_role, label) is correct
        self.monitor.check(from_role, self.self_role, func)

"""
Objectives:
1) pass the inner_role as an argument
2) check that decorator is applied correctly to the function:
The from role matched the sender of the message

"""

class role(object):
    def __init__(self, inner_role, from_role=None):
        self.inner_role = inner_role
        self.from_role  = from_role

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            # get it from self.parent
            role = getattr(args[0].actor, self.inner_role)
            role.check(self.from_role, f.__name__)
            if 'cid' in kwargs:
                print 'I am in join and I have the cid!', kwargs['cid']
                setattr(role, 'cid', kwargs['cid'])

            if not role.other_set:
                for r in role.others:
                    proxy = ActorProxy(config[role.prot][r],
                            id = r,
                            agent = args[0].actor.agent,
                            connection = args[0].actor.connection,
                            name = role.cid)
                    setattr(role, r, proxy)
                for key, val in role.group_roles.iteritems():
                    gr_actors = []
                    for i in range(0, prot_config[role.prot][val]):
                        proxy = ActorProxy(config[role.prot][key],
                            id=get_group_id(key, i),
                            agent = args[0].actor.agent,
                            connection = args[0].actor.connection,
                            name = role.cid)
                        gr_actors.append(proxy)
                    setattr(role, key, gr_actors)

                role.other_set = True
            if not self.from_role or self.from_role in role.others:
                if kwargs:
                    f(args[0], role, **kwargs)
                else:
                    f(args[0], role)
            else:
                raise NameError('Iuhu')
        wrapped_f.__name__ = f.__name__
        return wrapped_f

"""
Objestives:
    1) creates an instance of the ActorRole object and pass it to the class
"""
def protocol(inner_role, prot, self_role, roles, group_roles = {}, is_group = False):
    def class_rebuilder(cls):
        # Create an Actor instance
        role = ActorRole(cls, prot, self_role, roles, group_roles)
        setattr(cls, inner_role, role)
        if not is_group:
            setattr(cls, 'id', self_role)
        setattr(cls, 'role', self_role)
        #setattr(cls, 'name', self_role)
        return cls
    return class_rebuilder

from kombu import Exchange, Connection
from kombu.common import maybe_declare
from cell.agents import dAgent
from cell.actors import ActorProxy
import random

class ProtocolMailbox(Actor):
    class state(Actor.state):
        def start(self, prot_name):
            print 'In protocol start'
            exprot = Exchange(
                prot_name, type='fanout', auto_delete=False)
            conn = Connection()
            maybe_declare(exprot, conn.default_channel)
            roles = []
            for role, cls in role_mapping_config[prot_name].iteritems():
                if 'groups' not in prot_config[prot_name] or \
                    role not in prot_config[prot_name]['groups'].keys():

                    r = self.actor.agent.spawn(cls)
                    roles.append((r, role))

            if 'groups' in prot_config[prot_name]:
                groups = prot_config[prot_name]['groups']

                for role, number in groups.iteritems():
                    for i in range(0, prot_config[prot_name][number]):
                        r = self.actor.agent.spawn(role_mapping_config[prot_name][role],
                            id = get_group_id(role, i))
                        roles.append((r, get_group_id(role, i)))

            import time
            time.sleep(5)
            [r.add_binding(exprot, routing_key = role) for (r, role) in roles]
            print 'Protocol is declared!'
            return True

        def join(self, prot, cid):
            print 'In protocol mailbox join'

            """
            exprot = Exchange(
                cid, type='fanout', auto_delete=True)

            conn = Connection()
            maybe_declare(exprot, conn.default_channel)

            roles = []
            for role, cls in role_mapping_config[prot].iteritems():
                r = self.actor.agent.select(cls)
                roles.append(r)


            import time
            time.sleep(5)
            [r.add_binding(exprot, routing_key = r.id) for r in roles]
            """

            print 'Protocol is joined!'
            return True

    @classmethod
    def create(cls, prot, start_roles=[], group_roles = {}):
        conn = Connection()
        agent = dAgent(conn)
        pr = agent.select(ProtocolMailbox)

        exprot = Exchange(
            prot, type='fanout', auto_delete=False)

        cid = random.randint(1000, 2000)
        pr.cast('join', {'cid':str(cid)}, exchange = exprot)

        roles = {}
        for r in start_roles:
            e = ActorProxy(role_mapping_config[prot][r],
                id=r, agent = agent, connection = conn, name = cid)
            roles[r]  = e

        for r, val in group_roles.iteritems():
            gr_actors = []
            for i in range(0, val):
                proxy = ActorProxy(role_mapping_config[prot][r],
                    id=get_group_id(r, i),
                    agent = agent,
                    connection = conn,
                    name = cid)
                gr_actors.append(proxy)
            roles[r] = gr_actors

        return roles

def protocol_system_start(prot):
    conn = Connection()
    agent = dAgent(conn)
    pr = agent.spawn(ProtocolMailbox)
    pr.async_start_result.result()
    pr.call.start(prot_name=prot).result(timeout =10)

#e = Example()
#e.func('hello')

#ex = qualname(Example1)
#ex1 = qualname(Example)
#role_mapping = {'buyer': ex, 'seller':ex1}