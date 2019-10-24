# weko-tools


## JSON2Flat

### Convert strctured JSON object into flated JSON object

```
>>> from weko_tools.json2csv import JSON2Flat
>>> app = JSON2Flat()
>>> input = {'glossary': {'title': 'example glossary', 'GlossDiv': {'title': 'S', 'GlossList': {'GlossEntry': {'ID': 'SGML', 'SortAs': 'SGML', 'GlossTerm': 'Standard Generalized Markup Language', 'Acronym': 'SGML', 'Abbrev': 'ISO 8879:1986', 'GlossDef': {'para': 'A meta-markup language, used to create markup languages such as DocBook.', 'GlossSeeAlso': ['GML', 'XML']}, 'GlossSee': 'markup'}}}}}
>>> output = app.toFlat(input)
>>> output
{'$.glossary.GlossDiv.GlossList.GlossEntry.Abbrev': 'ISO 8879:1986', '$.glossary.GlossDiv.GlossList.GlossEntry.Acronym': 'SGML', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossDef.GlossSeeAlso[0]': 'GML', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossDef.GlossSeeAlso[1]': 'XML', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossDef.para': 'A meta-markup language, used to create markup languages such as DocBook.', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossSee': 'markup', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossTerm': 'Standard Generalized Markup Language', '$.glossary.GlossDiv.GlossList.GlossEntry.ID': 'SGML', '$.glossary.GlossDiv.GlossList.GlossEntry.SortAs': 'SGML', '$.glossary.GlossDiv.title': 'S', '$.glossary.title': 'example glossary'}
```

### Convert flated JSON object into strctured JSON object

```
>>> from weko_tools.json2csv import JSON2Flat
>>> app = JSON2Flat()
>>> input = {'$.glossary.GlossDiv.GlossList.GlossEntry.Abbrev': 'ISO 8879:1986', '$.glossary.GlossDiv.GlossList.GlossEntry.Acronym': 'SGML', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossDef.GlossSeeAlso[0]': 'GML', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossDef.GlossSeeAlso[1]': 'XML', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossDef.para': 'A meta-markup language, used to create markup languages such as DocBook.', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossSee': 'markup', '$.glossary.GlossDiv.GlossList.GlossEntry.GlossTerm': 'Standard Generalized Markup Language', '$.glossary.GlossDiv.GlossList.GlossEntry.ID': 'SGML', '$.glossary.GlossDiv.GlossList.GlossEntry.SortAs': 'SGML', '$.glossary.GlossDiv.title': 'S', '$.glossary.title': 'example glossary'}
>>> output = app.toStructure(input)
>>> output
{'glossary': {'GlossDiv': {'GlossList': {'GlossEntry': {'Abbrev': 'ISO 8879:1986', 'Acronym': 'SGML', 'GlossDef': {'GlossSeeAlso': ['GML', 'XML'], 'para': 'A meta-markup language, used to create markup languages such as DocBook.'}, 'GlossSee': 'markup', 'GlossTerm': 'Standard Generalized Markup Language', 'ID': 'SGML', 'SortAs': 'SGML'}}, 'title': 'S'}, 'title': 'example glossary'}}
```



## JSON2CSV

### Convert JSON objects into CSV file

```
>>> from weko_tools.json2csv import JSON2CSV
>>> import io
>>> app = JSON2CSV()
>>> d = [{'name':'john doe','age':30},{'name':'john doe','age':40}]
>>> f = io.StringIO()
>>> app.writeCSV(d,f)
>>> f.getvalue()
'"$.age","$.name"\r\n30,"john doe"\r\n40,"john doe"\r\n'
```

## Convert CSV file into JSON objects

```
>>> from weko_tools.json2csv import JSON2CSV
>>> f = io.StringIO('"$.age","$.name"\r\n30,"john doe"\r\n40,"john doe"\r\n')
>>> ret = app.readCSV(f)
>>> ret
[{'age': 30.0, 'name': 'john doe'}, {'age': 40.0, 'name': 'john doe'}]
```


## Unit Test

```
pytest -vv --cov=weko_tools --cov-report=html
```

