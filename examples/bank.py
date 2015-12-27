import celery
from cell.actors import Actor
from cell.agents import dAgent
from roles import role, protocol

# my_app = celery.Celery(broker='pyamqp://guest@localhost//')
# agent = dAgent(connection=my_app.broker_connection())
c, BankTransaction, T, A, SrcAcc, DestAcc = "c", "BankTransaction", "Teller", "A", "ScrAcc", "DestAcc"


@protocol(c, BankTransation, ScrAcc, [DestAcc, T])
@protocol(c1, BankTransation, DestAcc, [T, SrcAcc])
class Account(Actor):
    class state(Actor.state):
        @role(c, T)
        def credit(self, c1, data):
            c.DestAcc.call.debit()

        @role(c1, SrcAcc)
        def debit(self, c1):
            c.SrcAcc.call.reply()

        @role(c, DestAcc)
        def reply(self, c1):
            c.T.call.reply()

@protocol(c, BankTransaction, T, [A])
class Teller(Actor):
    class state(Actor.state):
        @role(c)
        def join(self, c):
            c.A.scatter.credit()
            return True

        @role(c, A)
        def reply(self, c):
            print 'Transaction completed'

def start_protocol(accounts):
    from kombu import Connection
    from cell.agents import dAgent
    from cell.examples import bank
    from cell.examples.bank import Teller, Account
    agent = dAgent(Connection())
    teller = agent.spawn(Teller)
    for i in range(1, accounts):
        agent.spawn(Account)
    import time
    time.sleep(3)
    teller.join().result()