#!/usr/bin/env python
# coding: utf-8

# In[2]:

#sklearn 0.19.2, imblearn 0.3.0
#please check the version of imblearn installed and mind the changes in api
import warnings
warnings.filterwarnings("ignore")


# In[3]:


import pandas
import numpy


# In[4]:


class instance():
    def __init__(self, label, features):
        self.label = label
        self.features = features


# In[5]:


class balanceness():
    
    def __init__(self, task):
        #task is a list of dict
        self.task = task
    
    def fit(self, instance):
        need_process = False
        trk = []
        for i in self.task:
            balance = self.balance_task(method = i["method"], 
                                  ratio = i["ratio"],
                                  k = i["k"],
                                  target = i["target"],
                                  floor = i["floor"],
                                  ceiling = i["ceiling"])
            trk.append((i["target"], i["ratio"], i["k"]))
            balance.fit(instance)
        
        #check if further process is needed
        import pandas
        import numpy
        length = len(instance.label)
        for i in trk:
            current = sum(instance.label == i[0])/length
            ideal = i[1]
            diff = abs(current - ideal)
            
            if diff >= 0.03:
                if length*current > length*ideal:
                    value = pandas.DataFrame(instance.features)
                    value["y"] = instance.label
                    label = value[value["y"] == i[0]]
                    result = pandas.concat((value[value["y"] == i[0]].sample(int(length*ideal)), 
                                    value[value["y"] != i[0]]), axis = 0)
                    instance.features, instance.label = numpy.array(result[result.columns[:-1]]), numpy.array(result[result.columns[-1]])
                    need_process = True
                    
                elif length*ideal > length*current:
                    from imblearn.over_sampling import SMOTE
                    smo = SMOTE(ratio = {
                        i[0]: int(length*ideal)
                    }, k_neighbors = i[2])
                    instance.features, instance.label = smo.fit_sample(instance.features, instance.label)
                    need_process = True
                    
        
        if need_process:
            target = [i[0] for i in trk]
            nontarget = [i for i in set(instance.label) if i not in target]
            value = pandas.DataFrame(instance.features)
            value["y"] = instance.label
        
            label = value[value["y"] == target[0]]
            for i in target:
                if i != target[0]:
                    label = pandas.concat((label, value[value["y"] == i]), axis = 0)
                
            nonvalue = value[value["y"] == nontarget[0]]
            for i in nontarget:
                if i != nontarget[0]:
                    nonvalue = pandas.concat((nonvalue, value[value["y"] == i]), axis = 0)
                
            result = pandas.concat((nonvalue.sample(int(length*(1 - sum([i[1] for i in trk])))), 
                        label), axis = 0)
            instance.features, instance.label = numpy.array(result[result.columns[:-1]]), numpy.array(result[result.columns[-1]])
        
    class balance_task():
        
        def __init__(self, method, ratio = 0.5, k = 5, target = 1, floor = None, ceiling = None):
            self.method = method
            self.ratio = ratio
            self.k = k
            self.target = target
            self.floor = floor
            self.ceiling = ceiling

        def smote(self, instance):
            from imblearn.over_sampling import SMOTE
            smo = SMOTE(ratio = {
                self.target: int(sum(instance.label != self.target)/(1-self.ratio) * self.ratio)
            }, k_neighbors = self.k)
            instance.features, instance.label = smo.fit_sample(instance.features, instance.label)

        def under_sampling(self, instance):
            import pandas
            import numpy
            value = pandas.DataFrame(instance.features)
            value["y"] = instance.label
            label = value[value["y"] == self.target]
            result = pandas.concat((value[value["y"] != self.target].sample(int(len(label)/self.ratio - len(label))), 
                                    value[value["y"] == self.target]), axis = 0)
            instance.features, instance.label = numpy.array(result[result.columns[:-1]]), numpy.array(result[result.columns[-1]])

        def fit(self, instance):
            labeln = sum(instance.label == self.target)
            nonlabeln = sum(instance.label != self.target)
            if (self.floor == None and self.ceiling == None) or (
                self.method == "under" and labeln/self.ratio >= self.floor) or (
                self.method == "over" and nonlabeln/(1 - self.ratio) <= self.ceiling):
                if self.method == "over":
                    self.smote(instance)
                else:
                    self.under_sampling(instance)

            elif self.method == "under" and labeln/self.ratio < self.floor:
                ratio_bak = self.ratio
                self.ratio = labeln/self.floor
                self.under_sampling(instance)
                self.ratio = ratio_bak
                self.smote(instance)

            elif self.method == "over" and nonlabeln/(1 - self.ratio) > self.ceiling:
                ratio_bak = self.ratio
                self.ratio = 1 - nonlabeln/self.ceiling
                self.smote(instance)
                self.ratio = ratio_bak
                self.under_sampling(instance)
            
            return instance

