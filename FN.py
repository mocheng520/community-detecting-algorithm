import networkx as nx
import time

class FN(object):
    def __init__(self,G):
        self.firstgraph = G.copy()
        self.G = nx.Graph()
        self.realG = G.copy()
        self.Q = 0
        self.part = []
        self.finapart = []



    def updata(self):

        while len(self.firstgraph.edges())>0:

            maxq = -999999999
            maxedge = []
            maxcompose = []

            for i in self.firstgraph.edges():
                Gclone = self.G.copy()
                Gclone.add_edge(i[0],i[1])

                q = self.calcQ(Gclone,[list(c) for c in list(nx.connected_components(Gclone))])

                if q > maxq:
                    maxedge = i
                    maxq = q
                    maxcompose = [list(c) for c in list(nx.connected_components(Gclone))]
            print(len(self.G.edges()))
            self.G.add_edge(maxedge[0],maxedge[1])
            self.firstgraph.remove_edge(maxedge[0],maxedge[1])

            if maxq >self.Q:
                self.Q = maxq
                self.part = maxcompose





    def calcQ(self,G,comp):
        m = len(self.firstgraph.edges())
        a = []
        e = []

        for community in comp:
            t = 0
            for node in community:

                t += self.realG.degree(node)
            a.append(t / float(2 * m))
        for community in comp:
            t = 0.0
            for i in community:
                for j in community:
                    if self.realG.has_edge(i, j):
                        t += 1.0
            e.append(t / float(2 * m))

        q = 0.0
        for ei, ai in zip(e, a):
            q += (ei - ai ** 2)

        return  q

if __name__ =="__main__":
    G=nx.read_gml('football真.gml')

    start = time.time()

    a= FN(G)

    a.updata()
    print('------------')

    print('模块度为',(a.Q))
    print('time:%d'%(time.time()-start))
    print('一共%d个社团' % (len(a.part)))
    for i in a.part:
        print(i)
