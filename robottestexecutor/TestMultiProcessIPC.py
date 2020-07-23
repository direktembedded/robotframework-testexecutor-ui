from multiprocessing import Process, Pipe

class myclass:
    one = 1
    two = 'two'

def f(conn):
    inst = myclass()
    conn.send([42, None, 'hello', inst])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    rc = parent_conn.recv()
    print(rc)   # prints "[42, None, 'hello']"
    a = rc[-1]
    print(a.one, a.two)
    p.join()