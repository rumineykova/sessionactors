__author__ = 'rn710'

role_mapping_config = {
    'Example':
            {'buyer':'cell.examples.basic.Pong',
             'seller':'cell.examples.basic.Ping',
             'buyer1': 'cell.examples.basic.Multi',
             'seller1': 'cell.examples.basic.Multi'},
    'Big':
           {'A':'cell.examples.big.Ping',
            'B':'cell.examples.big.Pong',
            'S':'cell.examples.big.Sink',},
    'SleepingBarber':
            {'B':'cell.examples.barber.Barber',
             'S':'cell.examples.barber.Selector',
             'C':'cell.examples.barber.Customer',
             'R':'cell.examples.barber.Room'},
    'CountProtocol':
            {'P':'cell.examples.count.Producer',
             'C':'cell.examples.count.Counter'},
    'CigaretteSmoker':
            {'A':'cell.examples.cigsmok.Arbitrer',
             'S':'cell.examples.cigsmok.Smoker'},
    'BankTransaction':
            {'T':'cell.examples.bank.Teller' ,
             'A':'cell.examples.bank.Account',
             'SrcAcc':'cell.examples.bank.Account',
             'DestAcc':'cell.examples.bank.Account'},
    'DiningPhilosophers':
            {'Ph':'cell.examples.dining_philosophers.Philosopher',
             'A':'cell.examples.dining_philosophers.Arbitrator'},
    'PCbounded':
            {'B':'cell.examples.pcbounded.Buffer',
             'C':'cell.examples.pcbounded.Consumer',
             'P':'cell.examples.pcbounded.Producer',},
    'KFork':
            {'M':'cell.examples.fork.Master',
             'W':'cell.examples.fork.Workers'},
    'Fibonacci':
            {'Ch':'cell.examples.fibonacci.Fibonacci',
             'P':'cell.examples.fibonacci.Fibonacci'},
    'ThreadRing':
            {'W':'cell.examples.thread_ring.Workers'}
}


prot_config = {
    'Example': {'n': 5},
    'SleepingBarber': {'n': 3, 'groups': {'C':'n'}},
    'CigaretteSmoker': {'n': 3, 'groups': {'S':'n'}},
    'DiningPhilosophers': {'n': 5, 'groups': {'Ph':'n'}},
    'ThreadRing': {'n': 5},
    'KFork': {'n': 5, 'groups': {'W':'n'}}
}

def get_group_id(role, id):
    return "%s_%s"%(role, id)

def get_num_from_id(id):
    id_array =  id.split('_')
    if len(id_array)>1:
        return int(id_array[1])
    else:
        return None
