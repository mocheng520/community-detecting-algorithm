```
import networkx as nx
import time

class GN(object):
    def __init__(self,G):
        self.firstgraph = G.copy()
        self.G = G
        self.Q = 0
        self.part = [list(c) for c in list(nx.connected_components(self.G))]
        self.finapart = [list(c) for c in list(nx.connected_components(self.G))]


    def updata(self):

        edge = max(nx.edge_betweenness_centrality(self.G).items(), key=lambda item: item[1])[0]
        self.G.remove_edge(edge[0],edge[1])
        self.part = [list(c) for c in list(nx.connected_components(self.G))]



    def calcQ(self):
        m = len(self.firstgraph.edges())
        a = []
        e = []

        for community in self.part:
            t = 0.0
            for node in community:
                t += self.firstgraph.degree(node)
            a.append( t / float( 2 * m ))
        for community in self.part :
            t = 0.0
            for i in community :
                for j in community :
                    if  self.firstgraph.has_edge(i,j):
                        t+=1.0
            e.append(t/float(2*m))

        q = 0.0
        for ei, ai in zip(e, a):
            q += (ei - ai **2)

        if q > self.Q:
            self.finapart = self.part
            self.Q = q

if __name__ == '__main__':

    G=nx.read_gml('football真.gml')
    a = GN(G)
    start = time.time()
    while len(a.G.edges()) > 1:
        print('已完成%d/%d'%(len(a.firstgraph.edges()) -len(a.G.edges())+1,len(a.firstgraph.edges())) )
        a.updata()
        a.calcQ()

    print('----------------------------------')
    print('最终模块度:',a.Q)
    print('time:%d' %(time.time()-start))
    print('共划分为 %d 个社团' % (len(a.finapart)))
    print('分别为：')
    for i in a.finapart:
        print (i)

    #可视化
    # newgraph = nx.Graph()
    # i = 0
    # for community in a.finapart:
    #     for node in community:
    #         newgraph.add_node(node,community = '%d' %(i))
    #     i+=1
    #
    # for edge in a.firstgraph.edges():
    #     a = edge[0]
    #     b = edge[1]
    #     newgraph.add_edge(a,b)
    #
    # nx.write_gml(newgraph,'shuchu.gml')
    #



                
```
