"""
sliding window
1 sort nums in each row, start with the first m/2 nums for each row
2 the local minimal cost is the gap between the smallest and the largest of all m/2 windows across rows
3 the m/2 window with the smallest element moves right by 1, and calculate the new local minimal cost.
4 if multiple rows' m/2 window share the same smallest num, we move the one with the smallest rightmost num after right move. e.g.

                         rows of [2,4,5], [2,3,6],  if window size==2,  
                         [2,4] and [2,3] have the same smallest num 2, 
                         we move [2,4] -->[4,5], because 6 in [3,6]>5, causing higher cost
5 get the global minimal cost and the num ranges causing the minimal cost
"""
arr=[[1,4,3],[3,5,6]]

arr=list(map(sorted,arr))                # sort each row
w=(m-1)//2                               # m/2 window length
index=Counter()                          # record where the begining of the m/2 window has reached for each row

low=[(arr[i][0],arr[i][w+1],i,0) for i in range(n)]
heapq.heapify(low)
h=max(arr[i][w] for i in range(n)) 

res=[float('inf'),[] ]                     # minimal cost, &  the low and high nums causing the minimal cost. 
while True:
    while index[low[0][2]]!=low[0][3]:   # remove invalid low values 
        heapq.heappop(low)
    
    l=low[0][0]                          # current low of all rows

    if res[0]==h-l:
       res[1]+=[(l,h)]                   # if multiple ranges have the same minimal cost, save all of them
   
    elif res[0]>h-l:
       res=[h-l,[(l,h)]]
       
    r,c=low[0][2:]
    if c+w==m-1:                         # stop the loop if a row's m/2 window can no longer move right 
        break
                                         # m/2 window for row r moves right by 1, from [c:c+w] to [c＋1，c+1+w]
    heapq.heappush(low, (arr[r][c+1],arr[r][min(c+1+w+1,m-1)],r,c+1))
    h=max(h,arr[r][c+1+w])
    index[r]+=1
           
# for all minimal cost ranges, check which one can cover more nums
ct=max(sum(bisect.bisect_right(row,h)-bisect.bisect_left(row,l) for row in arr) for l,h in res[1])

return ct*res[0] 
