# -*- coding: utf-8 -*-
# https://goessner.net/articles/JsonPath/

from jsonpath_rw.parser import JsonPathParser
from jsonpath_rw.lexer import JsonPathLexer
import copy
import re
import pandas as pd
import csv

from logging import getLogger,StreamHandler,DEBUG,Formatter
logger = getLogger(__name__) 
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class JSON2Flat():
    """
        JSON2FlatJSON convert from structured JSON to flat JSON using JSONPath. 
    """

    class JsonPathLexer(JsonPathLexer):
        '''
            A Lexical analyzer for JsonPath.
        '''

        def t_ID(self, t):
            r'[@$_]*[a-zA-Z_@]+[a-zA-Z0-9_@\-]*'
            t.type = self.reserved_words.get(t.value, 'ID')
            return t

    
    def parse(self,string):
        return JsonPathParser(lexer_class=self.JsonPathLexer).parse(string)

    def listAllPaths(self,json):
        """ list all JSONPath from JSON"""
        header = []
        for d in json:
            ret = self._getPath(json[d],"$."+d)
            if ret is not None:
                header = header + ret
        
        #header.sort()
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
            jsonpath_expr = self.parse(path)
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
                    if len(pathParts)==1:
                        currentIdx.append({key:flat[path]})
                    else:
                        tmp = {key : {}}
                        currentIdx.append(tmp)
                        currentIdx = tmp[key]
        return tree


    


class JSON2CSV():
    def writeCSV(self,data,file,quoting=csv.QUOTE_NONNUMERIC,lineterminator='\r\n'):
        ret = []
        app = JSON2Flat()
        for row in data:
            dat = app.toFlat(row)
            ret.append(dat)

        header = ret[0].keys()
        writer = csv.DictWriter(file,header,quoting=quoting,lineterminator=lineterminator)
        
        writer.writeheader()
        for d in ret:
            writer.writerow(d)


    def readCSV(self,file):
        ret = []
        app = JSON2Flat()
        df = pd.read_csv(file,quoting=csv.QUOTE_NONNUMERIC)
        for index,item in df.iterrows():
            dat = app.toStructure(item.to_dict())
            ret.append(dat)


        return ret



            
  

    

    