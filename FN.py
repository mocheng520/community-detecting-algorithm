import networkx as nx
import time

class FN(object):
    def __init__(self,G):
        self.G = nx.Graph()
        self.firstgraph = G
        self.dict = {}
        self.Q = 0
        self.finaQ = 0
        self.part = []
        self.m = len(G.edges())


    def pre(self):

           #初始化self.G
        for i in self.firstgraph.nodes():
            self.G.add_node(i)

            #算初始模块度
        q = []
        for node in self.firstgraph.nodes():
            q.append(self.firstgraph.degree(node))
        sum = 0
        for i in q:
            sum += -1.0 * float(i**2)/float(4 * self.m **2)
        self.Q = sum




    def calc_deltaQ(self, community_i, community_j):
        e = 0
        ai = 0
        aj = 0


        for node_i in community_i:
            for node_j in community_j:
                if self.firstgraph.has_edge(node_i, node_j):
                    e += 1

        for node_i in community_i:
            ai += self.firstgraph.degree(node_i)

        for node_j in community_j:
            aj += self.firstgraph.degree(node_j)

        q = 2.0 * (float(e) / float(2 * self.m) - float(ai) * float(aj) / float(4 * self.m ** 2))


        return q


    def calc(self):

        maxq = -999
        maxedge = (-1,-1)
        for i in self.firstgraph.edges():

            community_a = []
            community_b = []



            for component in nx.connected_components(self.G):
                if i[0] in component and i[1] in component:break

                if i[0] in component: community_a = component
                if i[1] in component: community_b = component

    
            if len(community_a) == 0 : continue


            q = self.calc_deltaQ(community_a, community_b)
            #记录每一轮的最大ΔQ和对应的边
            if q > maxq:
                maxq = q
                maxedge = i
        self.Q += maxq
        if  maxedge[0] != -1:
            self.G.add_edge(maxedge[0], maxedge[1])

        #如果本轮迭代的Q继续增大，则记录此时对应的社团情况
        if self.Q > self.finaQ:

            self.finaQ = self.Q

            self.part = list(nx.connected_components(self.G))


if __name__== '__main__':


    start = time.time()

    G = nx.read_gml('football真.gml')

    a = FN(G)
    a.pre()
    m = a.m
    while  m>0:
        print(a.m - m,'/',a.m)
        m-=1
        a.calc()
    print(a.finaQ)
    print('耗时：',time.time()-start)
    print('一共 %d个社团'%(len(a.part)))

    for i in a.part:
        print(i)

