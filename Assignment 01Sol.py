import snap
import random


    
def wikiVotingNetwork():
    
    Component = snap.TIntPrV()
    #Loding the graph
    Wiki = snap.LoadEdgeList(snap.PNGraph, "Wiki-Vote.txt", 0, 1)
    #Printing Number of Nodes in the Graph
    print "Number of Nodes: ", Wiki.GetNodes()
    #Printing Number of Edges in the Graph
    print "Number of Edges: ", Wiki.GetEdges()
    #Printing Number of Directed Edges in the Graph
    print "Number of Directed Edges: ",snap.CntUniqDirEdges(Wiki)
    #Printing Number of Un-Directed Edges in the Graph
    print "Number of Undirected Edges: ",snap.CntUniqUndirEdges(Wiki)
    #Printing Number of Directed Edges in the Graph
    print "Number of Self-Edges: ", snap.CntSelfEdges(Wiki)
    #Printing Number of Zero InDeg Nodes in the Graph
    print "Number of Zero InDeg Nodes: ",snap.CntInDegNodes(Wiki, 0)
    #Printing Number of Zero OutDeg Nodes in the Graph
    print "Number of Zero OutDeg Nodes: ",snap.CntOutDegNodes(Wiki, 0)
    #Printing Node ID with maximum degree in the Graph
    print "Node ID with maximum degree: ",snap.GetMxDegNId(Wiki)
    
    snap.GetSccSzCnt(Wiki,Component)
    
    for comp in Component:
        #printing number of strongly connected components with size
        print "Size: %d - Number of Strongly Connected Components: %d" % (comp.GetVal1(),comp.GetVal2())
    #printing size of largest connected components    
    print "Size of largest connected component: ", snap.GetMxSccSz(Wiki)
    
    snap.GetWccSzCnt(Wiki,Component)
    
    for comp in Component:
        #printing number of weekly connected components with size
        print "Size: %d - Number of Weekly Connected Component Wikipedia: %d" % (comp.GetVal1(), comp.GetVal2())

    #printing size of weekly connected components    
    print "Size of Weakly connected component: ", snap.GetMxWccSz(Wiki)
    #plotting out-degree distribution
    snap.PlotOutDegDistr(Wiki, "wiki-analysis", "Directed graph - Out-Degree Distribution")
    

def clustCoefficient(G):
    
     #defining arrays   
    clusteringDict = []
    
    array = []
    #appending node ids in an array
    for s in G.Nodes():
        
        array.append(s.GetId())
        
     #checking if the length of an array is greater than 2   
    if (len(array) > 2):
        
        for item in array:
            
            #defining arrays
            
            neighbours = []
            nodesWithMutualNeighbuors = []
            #defining a vector
            NodeVec = snap.TIntV()
            snap.GetNodesAtHop(G, item, 1, NodeVec, False)
            ##Appending neighbours Nodes at Hop in the vector
            for item in NodeVec:
                
                neighbours.append(item)
             #appending second layer neighbours in the vector   
            for item2 in NodeVec:
                
                 SecondNodeVec = snap.TIntV()
                 snap.GetNodesAtHop(G, item2, 1, SecondNodeVec, False)
                 
                 for second_layer_neighbour in SecondNodeVec:
                    
                    if second_layer_neighbour in neighbours:
                       nodesWithMutualNeighbuors.append(second_layer_neighbour)
                    
            
            nodesWithMutualNeighbuors = list(nodesWithMutualNeighbuors)
            
            clusteringCoefficientOfNode = 0
            #applying clustering co-efficient formula
            if len(nodesWithMutualNeighbuors):
                
                clusteringCoefficientOfNode =  (float(len(nodesWithMutualNeighbuors)))/((float(len(NodeVec)) * (float(len(NodeVec)) - 1)))
            
            clusteringDict.append(clusteringCoefficientOfNode)
                
    
    
    
    else:
        pass
    
    #finding the average value
    clust_avg_value = 0
    
    if len(clusteringDict) is not 0:
        
        for value in clusteringDict:
            
            clust_avg_value = clust_avg_value + value
            
        return clust_avg_value/ len(clusteringDict)
    else:
        
        return 0



def erdosRenyi(G,p):
    #Iterating all the nodes 
    for i in G.Nodes():
    #Checking single node edges to all the nodes   
        for j in G.Nodes():
    # Removing the self nodes      
            if i.GetId() != j.GetId():
    #generating a random value         
                r = random.random()
                
    #Checking if random value is smaller then the probability user has provided           
                if r <= p:
    #Adding Edges to the Nodes                
                    G.AddEdge(i.GetId(),j.GetId())
                    
                else:
                    
                    continue
    


def smallWorldRandomNetwork(G,e):
    
    #Creating an empty array to store the sys_id's of nodes
    a = []
    #Creating a variable to keep track of the back neighbor of neighbor    
    backEdge = -2
    #Creating a variable to keep track of the front neighbor of neighbor
    frontEdge = 2
    #Creating a variable to keep track of the number of random edges
    count = 0
    
   #Storing the sys_id's of nodes in an array
    for s in G.Nodes():
        a.append(s.GetId())
    #Adding Edges to Nodes to form a ring
    for ind in xrange(len(a)):
        if (ind+1) < len(a):
            second = a[ind+1]
            G.AddEdge(a[ind],second)
        else:
            G.AddEdge(a[0],a[len(a)-1])
    #Adding edges to the neighbor of neighbors nodes       
    for dx in xrange(len(a)):
        if (dx+1) < len(a):
            
            if frontEdge < len(a):
                G.AddEdge(a[dx],a[frontEdge])
                frontEdge = frontEdge + 1

            if backEdge < len(a):
                G.AddEdge(a[dx],a[backEdge])
                backEdge = backEdge + 1

    
    #Adding Random Edges to the unconnected nodes
    for x in xrange(len(a)):
     
        for y in xrange(len(a)):
        
            if a[x] != a[y]:
                
                if not G.IsEdge(a[x],a[y]):
                    
                   if count < e:
                       
                       G.AddEdge(a[x],a[y])
                       
                       count = count + 1
                       
                       random.shuffle(a)
                                          
    



def main():
    
    Component = snap.TIntPrV()
    #loading the real world graph
    realWorld = snap.LoadEdgeList(snap.PUNGraph, "CA-HepTh.txt", 0, 1)
    #deleting the self-edges from the graph
    snap.DelSelfEdges(realWorld)
    #calling the function
    wikiVotingNetwork()
     #Taking number of nodes in a graph from real world network
    n = realWorld.GetNodes()
    #Generating an Undirected Graph
    G = snap.TUNGraph.New()
    #Taking number of edges in a graph from user
    e =  int(raw_input('Enter the number of Random Edges : '))
    
    p = float(raw_input('Enter the Probability of Edges between Nodes from 0-1  : '))
    #Generating Number of Nodes
    for i in range(n):
    #Adding Nodes into the graph
        G.AddNode(i)
    #calling the function        
    erdosRenyi(G,p)
    #Printing the Clustering 
    print 'Erdos Renyi Clustering Co-efficient: ',clustCoefficient(G)
    
    diam = snap.GetBfsFullDiam(G, 9877, False)
    #printing the diameter
    print 'Erdos Renyi Diameter: ',diam
    #plotting the graph
    snap.PlotOutDegDistr(G, "Erdos-Renyi", "Un-Directed graph - Out-Degree Distribution")
    
    snap.GetSccSzCnt(G,Component)
    
    for comp in Component:
        #printing number of strongly connected components with size
        print "Size: %d - Number of Connected Component in Erdos-Renyi: %d" % (comp.GetVal1(), comp.GetVal2())
    #printing fraction of nodes and edges 
    print "Fraction of Nodes and Edges in Erdos Renyi: ",snap.GetMxSccSz(G)
    #Drawing a Erdos Renyi Graph
    snap.DrawGViz(G, snap.gvlDot, "erdosRenyi1.png","Erdos Renyi")
    #calling the function
    smallWorldRandomNetwork(G,e)
    #printing the clustering coefficient
    print 'Small World Random Network Clustering Co-efficient: ',clustCoefficient(G)
    
    diam = snap.GetBfsFullDiam(G, 9877, False)
    #printing the diameter
    print 'Small World Random Network Diameter: ',diam
   
    snap.GetSccSzCnt(G,Component)
    
    for comp in Component:
        
        #printing number of strongly connected components with size
        
        print "Size: %d - Number of Connected Component in Small World: %d" % (comp.GetVal1(), comp.GetVal2())
    #fraction of nodes and edges in small world
    print "Fraction of Nodes and Edges in Small World: ",snap.GetMxSccSz(G)
    #plotting the graph
    snap.PlotOutDegDistr(G, "Small-World", "Un-Directed graph - Out-Degree Distribution")
    #drawinf the graph
    snap.DrawGViz(G, snap.gvlDot, "smallWorld1.png","Small World Random Network")
    #calculating the clustering co-efficient
    print 'Real World Random Network Clustering Co-efficient: ',clustCoefficient(realWorld)
    
    diam = snap.GetBfsFullDiam(G, 9877, False)
    
    print 'Real World Random Network Diameter: ',diam
    
    snap.GetSccSzCnt(realWorld,Component)
    
    for comp in Component:
        #printing number of strongly connected components with size
        
        print "Size: %d - Number of Weekly Connected Component in Real World: %d" % (comp.GetVal1(), comp.GetVal2())
    #printing fraction of nodes and edges
    print "Fraction of Nodes and Edges in Small World: ",snap.GetMxSccSz(realWorld)
    #plotting the real world network graph
    snap.PlotOutDegDistr(realWorld, "real-World", "Un-Directed graph - Out-Degree Distribution")
    #Drawing Real WOrld Graph
    snap.DrawGViz(realWorld, snap.gvlDot, "realWorld.png","Real World Random Network")
main()


