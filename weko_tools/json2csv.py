# -*- coding: utf-8 -*-
# https://goessner.net/articles/JsonPath/

from jsonpath_ng.ext import parse
import copy
import re
import csv

class JSON2Flat():
    """
        JSON2FlatJSON convert from structured JSON to flat JSON using JSONPath. 
    """
    
    def listAllPaths(self,json):
        """ list all JSONPath from JSON"""
        header = []
        for d in json:
            ret = self._getPath(json[d],"$."+d)
            if ret is not None:
                header = header + ret
        
        header.sort()
        return header
    
    def _getPath(self,doc,path):
        result = []
        if type(doc) is dict:
            for d in doc:
                ret = self._getPath(doc[d],path+"."+d)
                if ret is not None:
                    result = result + ret
        elif type(doc) is list:
            idx = 0
            for d in doc:
                ret = self._getPath(d,path+"["+str(idx)+"]")
                if ret is not None:
                    result = result + ret
                idx = idx + 1
        else:
            result.append(path)
        
        return result
    
    def listAllValues(self,json,paths):
        result = []
        for path in paths:
            jsonpath_expr = parse(path)
            ret = jsonpath_expr.find(json)
            for match in ret:
                result.append(match.value)
        
        return result
    
    def toFlat(self,json):
        result = {}
        paths = self.listAllPaths(json)
        values = self.listAllValues(json,paths)
        for i in range(len(paths)):
            result[paths[i]] = values[i]

        return result 
    
    def toStructure(self,flat):
        tree = {}
        for path in flat:
            no = 0
            pathParts = path.split('.')
            currentIdx = tree
            
            while len(pathParts)>1:
                pathParts.pop(0)
                p = re.compile(".*\\[([0-9]+)\\]")
                ret = p.match(pathParts[0])
                if ret is not None:
                    no = int(ret.groups()[0])
                key = re.sub('\\[[0-9]+\\]',"",pathParts[0])
                if type(currentIdx) is dict:
                    nextIdx = currentIdx.get(key)
                    if nextIdx is None:
                        if pathParts[0] == key:
                            if len(pathParts)==1:
                                nextIdx = flat[path]
                                currentIdx[key] = nextIdx
                                currentIdx = nextIdx
                            else:
                                nextIdx = {}
                                currentIdx[key] = nextIdx
                                currentIdx = currentIdx[key]
                        else:
                            if len(pathParts)==1:
                                nextIdx = flat[path]
                                currentIdx[key] = [nextIdx]
                                currentIdx = currentIdx[key]
                            else:
                                nextIdx = []
                                currentIdx[key] = nextIdx
                                currentIdx = currentIdx[key]
                    else:
                        if type(nextIdx) is list:
                            if len(nextIdx) > no:
                                currentIdx = nextIdx[no]
                            else:
                                if len(pathParts)==1:
                                    tmp = flat[path]
                                else:
                                    tmp = {}
                                nextIdx.append(tmp)
                                currentIdx = tmp
                        elif type(nextIdx) is dict:
                            currentIdx = nextIdx
                elif type(currentIdx) is list:
                    p = re.compile(".*\\[([0-9]+)\\]")
                    ret = p.match(pathParts[0])
                    if ret is None:
                        if len(currentIdx) == 0:
                            if len(pathParts)==1:
                                currentIdx.append({key:flat[path]})
        return tree


class JSON2CSV():
    def writeCSV(self,data,file):
        ret = []
        app = JSON2Flat()
        for row in data:
            dat = app.toFlat(row)
            ret.append(dat)

        header = ret[0].keys()
        writer = csv.DictWriter(file,header, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in ret:
            writer.writerow(d)


    def readCSV(self,file):
        ret = []
        app = JSON2Flat()
        reader = csv.DictReader(file, quoting=csv.QUOTE_NONNUMERIC)

        for row in reader:
            dat = app.toStructure(row)
            ret.append(dat)
        
        return ret



            
  

    

    