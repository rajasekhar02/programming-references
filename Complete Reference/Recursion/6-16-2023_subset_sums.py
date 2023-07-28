class Solution:
    def subsetSums(self, arr, N):
        return self.recur(arr, 0, N)

    def recur(self, arr, pos, N):
        if N == 0:
            return [0]
        lis = self.recur(arr, pos + 1, N - 1)
        sizeOfLis = len(lis)
        newList = lis
        for i in range(0, sizeOfLis):
            newList.append(lis[i] + arr[pos])
        return newList

    def subsetSumsItr(self, arr, N):
        # code here
        totalSubsets = 1 << N
        # print(totalSubsets)
        sums = [0]
        for i in range(1, totalSubsets):
            j = 0
            pos = 1 << j
            subSetSum = 0
            while pos <= i:
                if pos & i:
                    subSetSum += arr[j]
                j += 1
                pos = 1 << j
            sums.append(subSetSum)
        return sums