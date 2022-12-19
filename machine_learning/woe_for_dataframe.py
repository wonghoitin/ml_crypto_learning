#!/usr/bin/env python
# coding: utf-8

# In[1]:


def woe(data):
    import math
    large1, large0 = sum(data[data.columns[-1]]), sum(data[data.columns[-1]] == False)
    for column in data.columns[:-1]:
        local = {}
        for unique in set(data[column].unique()):
            local_1, local_0 = sum(data[data[column] == unique][data.columns[-1]]), sum(data[data[column] == unique][data.columns[-1]] == False)
            if local_1 == 0:
                local[unique] = 0
            elif local_0 != 0:
                local[unique] = (
                                    math.log(
                                            (local_1/large1)/(local_0/large0)  
                                            )
                                )
            else:
                local[unique] = (
                                (local_1/large1)
                                )
        temp = []
        for row in data[column]:
            temp.append(local[row])
        data[column] = temp
    return data

