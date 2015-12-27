from cell.actors import Actor
from roles import role, protocol

#my_app = celery.Celery(broker='pyamqp://guest@localhost//')
#agent = dAgent(connection=my_app.broker_connection())
c, Fib, Ch, P = "c", "Fibonacci", "Ch", "P"

@protocol(c, Fib, Ch, [P, Ch], True)
class Fibonacci(Actor):
    class state(Actor.state):
        def join(self, first = False, num = 0):
            self.ready = False
            self.current = 0
            self.first = first
            self.num = num
            return True

        @role(c, P)
        def req(self, c, n):
                if n<=2:
                    c.P.call.res(1)
                else:
                    fib1 = c.subprotocol(Fib,
                        P=c.role, Ch=Fibonacci)
                    fib1.C.call.req(n = n-1)

                    fib2 = c.subprotocol(Fib,
                        P=c.role, Ch= Fibonacci)

                    fib2.C.call.req(n = n-2)

        @role(c, Ch)
        def res(self, c, n):
            if self.ready:
                if self.is_first:
                    print 'The result is', n + self.current
                else:
                    c.P.call.res(n + self.current)
            else:
                self.ready = True
                self.current = n