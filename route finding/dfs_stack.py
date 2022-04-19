import csv
from collections import defaultdict

def dfs(start, end):
    # Begin your code (Part 2)
    """
        Open edges.csv first,then use defaultdict to construct lists named dict and visited.
        'dict' is used to save the end node,distance and speed limit of certain start node.
        'visited' is used to save whether the node is searched or not.
        Use readlines and split to store every datas,then I construct list named explored,fronter
        and distance.
        'explored' is used to save the order of nodes that we should search.
        'fronter' is used to save the parent of the node.
        Pop the last data of explored to find out the start node(the node is named 'begin') we use 
        it to find out the end node from dict(the end node is named 'final').
        If 'final' is not visited,append it to explored and plus one to num_visited.
        'dist' is the sum of the distance in edges.csv of the number in fronter. 
        Finally,use path to save the nodes that are included in the path,and change it to 
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
        visited[detail[0]]=False
    num_visited=0
    explored=[]
    explored.append(start)
    visited[str(start)]=True
    fronter=defaultdict(str)
    while len(explored)!=0:
        begin=str(explored.pop())
        for i in range(len(dict[begin])):
            final=dict[begin][i][0]
            if visited[final]!=True:
                fronter[final]=begin
                visited[str(final)]=1
                explored.append(final)
                num_visited+=1
                if final==str(end):
                    explored.clear()
                    break
                
    path=[]
    dist=0
    path.append(str(end))
    while path[0]!=str(start):
        for i in range(len(dict[fronter[path[0]]])):
            if dict[fronter[path[0]]][i][0]==path[0]:
                dist+=float(dict[fronter[path[0]]][i][1])
        path.insert(0,fronter[path[0]])
    for i in range(len(path)):
        path[i]=int(path[i]) 
    
    return path,dist,num_visited
    raise NotImplementedError("To be implemented")
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
