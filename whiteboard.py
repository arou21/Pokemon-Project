# Find Single Number
# Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.
# Example 1:
# Input: nums = [2,2,1]
# Output: 1
# Example 2:
# Input: nums = [4,1,2,1,2]					
# Output: 4
# Example 3:
# Input: nums = [1]
# Output: 1


nums1 = [2,2,1]
nums2 = [4,1,2,1,2]  
nums3 = [1]

def findSingle(li):
    for num in li:
        if li.count(num) == 1:
            print(num)
            return num

findSingle(nums1)
findSingle(nums2)
findSingle(nums3)

def findSingle2(li):
    empty = {}

    for num in li:
        if num in empty:
            empty[num] += 1
        else:
            empty[num] = 1
            
    for k, v in empty.items():
        if v == 1:
            print(k)
            return k
    # print(empty)
    #       


findSingle2(nums1)
findSingle2(nums2)
findSingle2(nums3)