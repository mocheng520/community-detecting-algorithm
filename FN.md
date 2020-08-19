```

import networkx as nx
import time

class FN(object):
    def __init__(self,G):
        self.G =nx.Graph()
        self.firstgraph = G
        self.part = []
        self.finapart = []
        self.used_edge = []
        self.finaQ =0
        self.Q = 0

    def pre(self,G):
        self.G.add_nodes_from([i for i in G.nodes()])
    def updata(self,G):
        self.pre(G)
        maxcomponent =[]
        maxG = self.G
        maxedge = list(self.firstgraph.edges())

        for num in range(len(self.firstgraph.edges())):
            print('已完成%d/%d'%(num+1,len(self.firstgraph.edges())))
            maxq = -99

            for i in self.firstgraph.edges():
                if not ( list(i) in self.used_edge):#这里可以用字典优化下，可以把O（N）优化到O（1），有空再来⛏吧（2020.8.19/20:54）

                    Gclone = self.G.copy()#一定要G.copy（），因为python传引用,翻了一天的资料，差点怀疑人生，最后发现这里错了（2020.8.19/20:10）

                    Gclone.add_edge(list(i)[0],list(i)[1])


                    component = [list(c) for c in list(nx.connected_components(Gclone))]
                    q = self.calcQ(Gclone,component)

                    if q >= maxq:
                        maxq = q
                        maxcomponent = component
                        maxedge = list(i)


            self.used_edge.append(maxedge)

            self.G.add_edge(maxedge[0],maxedge[1])

            if maxq >self.finaQ:
                    self.finaQ = maxq
                    self.finapart = maxcomponent







    def calcQ(self,Gclone,component):
        m = len(self.firstgraph.edges())
        a = []
        e = []




        for community in component:
            t = 0.0
            for node in community:
                t += self.firstgraph.degree(node)
            a.append(t / float(2 * m))
        for community in component:
            t = 0.0
            for i in community:
                for j in community:
                    if self.firstgraph.has_edge(i, j):
                        t += 1.0
            e.append(t / float(2 * m))

        q = 0.0
        for ei, ai in zip(e, a):

            q += (ei - ai ** 2)

        return q



if __name__ =="__main__":
    G=nx.read_gml('football真.gml')

    start = time.time()

    a= FN(G)

    a.updata(G)
    print('------------')

    print('模块度为：%d'%(a.finaQ))
    print('time:%d'%(time.time()-start))
    print('一共%d个社团' % (len(a.finapart)))
    for i in a.finapart:
        print(i)

```
