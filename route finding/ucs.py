import csv
from collections import defaultdict


def ucs(start, end):
    # Begin your code (Part 3)
    """
        Open edges.csv first,then use defaultdict to construct lists named dict and visited.
        'dict' is used to save the end node,distance and speed limit of certain start node.
        'visited' is used to save whether the node is searched or not.
        Use readlines and split to store every datas,then I construct list named explored,fronter
        and distance.
        'explored' is used to save the order of nodes that we should search.
        'distance' is used to save the distance from the start node to the end node.
        'fronter' is used to save the parent of the node.
        Set 'minimum' as infinite,then compare minimum to each distace of the data of
        explored,if it is less than minimum,it is changed to become minimum.Use the index of 
        this data to find out the start node(the node is named 'begin') we use it to find out the
        end node from dict(the end node is named 'final').
        num_visited pluses one.
        If 'final' is not visited,compare the distance from start to final and the distance 
        from start to start node + distance in edges.csv,and change it to the smaller one.
        Finally,use path to save the nodes that are included in the path,andn change it to 
        integer.

    """
    file=open('edges.csv')
    dict=defaultdict(list)
    visited=defaultdict(str)
    lines=file.readlines()

    for line in lines:
        detail=line.split(',')
        data=[]
        data.append(detail[1])
        data.append(detail[2])
        data.append(detail[3].replace("\n",""))
        dict[detail[0]].append(data)
        dict[detail[0]].sort(key=lambda s:s[1])
        visited[detail[0]]=False
    num_visited=0
    explored=[]
    explored.append(start)
    visited[str(start)]=True
    fronter=defaultdict(str)
    distance=defaultdict(float)
    distance[start]=0
    while len(explored)!=0:
        minimum=float("inf")
        index=0
        for i in range(len(explored)):
            if distance[explored[i]]<minimum:
                minimum=distance[explored[i]]
                index=i
        begin=str(explored.pop(index))
        visited[begin]=1
        num_visited+=1
        if begin==str(end):
            explored.clear()
            dist=distance[str(end)]
            break
        for i in range(len(dict[begin])):
            final=dict[begin][i][0]
            if visited[final]!=1:
                if final not in explored:
                    explored.append(final)
                if final in distance:
                    if distance[final]>distance[begin]+float(dict[begin][i][1]):
                        fronter[final]=begin
                        distance[final]=distance[begin]+float(dict[begin][i][1])
                else:
                    fronter[final]=begin
                    distance[final]=distance[begin]+float(dict[begin][i][1])
        distance[index]=float("inf")
                
    path=[]
    path.append(str(end))
    while path[0]!=str(start):
        path.insert(0,fronter[path[0]])
    for i in range(len(path)):
        path[i]=int(path[i]) 
    return path,dist,num_visited
    raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
