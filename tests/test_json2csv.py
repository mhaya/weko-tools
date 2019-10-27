# -*- coding: utf-8 -*-

import pytest
from weko_tools.json2csv import JSON2Flat,JSON2CSV
import io

@pytest.mark.parametrize('input,output', [
    (
        {"id": 1, "name":"john doe"},
        ['$.id','$.name']
    ),
    (
        {'$schema': 'https://json-schema.org/draft/2019-09/schema', '$id': 'https://json-schema.org/draft/2019-09/output/schema', 'description': 'A schema that validates the minimum requirements for validation output', 'oneOf': [{'$ref': '#/$defs/flag'}, {'$ref': '#/$defs/basic'}, {'$ref': '#/$defs/detailed'}, {'$ref': '#/$defs/verbose'}], '$defs': {'outputUnit': {'properties': {'valid': {'type': 'boolean'}, 'keywordLocation': {'type': 'string', 'format': 'uri-reference'}, 'absoluteKeywordLocation': {'type': 'string', 'format': 'uri'}, 'instanceLocation': {'type': 'string', 'format': 'uri-reference'}, 'errors': {'$ref': '#/$defs/outputUnitArray'}, 'annotations': {'$ref': '#/$defs/outputUnitArray'}}, 'required': ['valid', 'keywordLocation', 'instanceLocation'], 'allOf': [{'if': {'properties': {'valid': {'const': False}}}, 'then': {'required': ['errors']}}, {'if': {'oneOf': [{'properties': {'keywordLocation': {'pattern': '.*/$ref/.*'}}}, {'properties': {'keywordLocation': {'pattern': '.*/$recursiveRef/.*'}}}]}, 'then': {'required': ['absoluteKeywordLocation']}}]}, 'outputUnitArray': {'type': 'array', 'items': {'$ref': '#/$defs/outputUnit'}}, 'flag': {'properties': {'valid': {'type': 'boolean'}}, 'required': ['valid']}, 'basic': {'$ref': '#/outputUnit'}, 'detailed': {'$ref': '#/outputUnit'}, 'verbose': {'$ref': '#/outputUnit'}}},
        ['$.$schema', '$.$id', '$.description', '$.oneOf[0].$ref', '$.oneOf[1].$ref', '$.oneOf[2].$ref', '$.oneOf[3].$ref', '$.$defs.outputUnit.properties.valid.type', '$.$defs.outputUnit.properties.keywordLocation.type', '$.$defs.outputUnit.properties.keywordLocation.format', '$.$defs.outputUnit.properties.absoluteKeywordLocation.type', '$.$defs.outputUnit.properties.absoluteKeywordLocation.format', '$.$defs.outputUnit.properties.instanceLocation.type', '$.$defs.outputUnit.properties.instanceLocation.format', '$.$defs.outputUnit.properties.errors.$ref', '$.$defs.outputUnit.properties.annotations.$ref', '$.$defs.outputUnit.required[0]', '$.$defs.outputUnit.required[1]', '$.$defs.outputUnit.required[2]', '$.$defs.outputUnit.allOf[0].if.properties.valid.const', '$.$defs.outputUnit.allOf[0].then.required[0]', '$.$defs.outputUnit.allOf[1].if.oneOf[0].properties.keywordLocation.pattern', '$.$defs.outputUnit.allOf[1].if.oneOf[1].properties.keywordLocation.pattern', '$.$defs.outputUnit.allOf[1].then.required[0]', '$.$defs.outputUnitArray.type', '$.$defs.outputUnitArray.items.$ref', '$.$defs.flag.properties.valid.type', '$.$defs.flag.required[0]', '$.$defs.basic.$ref', '$.$defs.detailed.$ref', '$.$defs.verbose.$ref']
    ),
    (
        {'@context': 'https://schema.org/', '@type': 'Dataset', 'name': 'NCDC Storm Events Database', 'description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', 'url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', 'sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', 'identifier': ['https://doi.org/10.1000/182', 'https://identifiers.org/ark:/12345/fk1234'], 'keywords': ['ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE'], 'creator': {'@type': 'Organization', 'url': 'https://www.ncei.noaa.gov/', 'name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', 'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+1-828-271-4800', 'email': 'ncei.orders@noaa.gov'}}, 'includedInDataCatalog': {'@type': 'DataCatalog', 'name': 'data.gov'}, 'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'CSV', 'contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp'}, {'@type': 'DataDownload', 'encodingFormat': 'XML', 'contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510'}], 'temporalCoverage': '1950-01-01/2013-12-18', 'spatialCoverage': {'@type': 'Place', 'geo': {'@type': 'GeoShape', 'box': '18.0 -65.0 72.0 172.0'}}},
        ['$.@context', '$.@type', '$.name', '$.description', '$.url', '$.sameAs', '$.identifier[0]', '$.identifier[1]', '$.keywords[0]', '$.keywords[1]', '$.keywords[2]', '$.keywords[3]', '$.creator.@type', '$.creator.url', '$.creator.name', '$.creator.contactPoint.@type', '$.creator.contactPoint.contactType', '$.creator.contactPoint.telephone', '$.creator.contactPoint.email', '$.includedInDataCatalog.@type', '$.includedInDataCatalog.name', '$.distribution[0].@type', '$.distribution[0].encodingFormat', '$.distribution[0].contentUrl', '$.distribution[1].@type', '$.distribution[1].encodingFormat', '$.distribution[1].contentUrl', '$.temporalCoverage', '$.spatialCoverage.@type', '$.spatialCoverage.geo.@type', '$.spatialCoverage.geo.box']
    )
])
def test_listAllPaths(input, output):
        app = JSON2Flat()
        path = app.listAllPaths(input)
        assert output == path

@pytest.mark.parametrize('json,paths,output', [
    (
        {"id": 1, "name":"john doe"},
        ['$.id','$.name'],
        [1,'john doe']
    ),
    (
        {'$schema': 'https://json-schema.org/draft/2019-09/schema', '$id': 'https://json-schema.org/draft/2019-09/output/schema', 'description': 'A schema that validates the minimum requirements for validation output', 'oneOf': [{'$ref': '#/$defs/flag'}, {'$ref': '#/$defs/basic'}, {'$ref': '#/$defs/detailed'}, {'$ref': '#/$defs/verbose'}], '$defs': {'outputUnit': {'properties': {'valid': {'type': 'boolean'}, 'keywordLocation': {'type': 'string', 'format': 'uri-reference'}, 'absoluteKeywordLocation': {'type': 'string', 'format': 'uri'}, 'instanceLocation': {'type': 'string', 'format': 'uri-reference'}, 'errors': {'$ref': '#/$defs/outputUnitArray'}, 'annotations': {'$ref': '#/$defs/outputUnitArray'}}, 'required': ['valid', 'keywordLocation', 'instanceLocation'], 'allOf': [{'if': {'properties': {'valid': {'const': False}}}, 'then': {'required': ['errors']}}, {'if': {'oneOf': [{'properties': {'keywordLocation': {'pattern': '.*/$ref/.*'}}}, {'properties': {'keywordLocation': {'pattern': '.*/$recursiveRef/.*'}}}]}, 'then': {'required': ['absoluteKeywordLocation']}}]}, 'outputUnitArray': {'type': 'array', 'items': {'$ref': '#/$defs/outputUnit'}}, 'flag': {'properties': {'valid': {'type': 'boolean'}}, 'required': ['valid']}, 'basic': {'$ref': '#/outputUnit'}, 'detailed': {'$ref': '#/outputUnit'}, 'verbose': {'$ref': '#/outputUnit'}}},
        ['$.$schema', '$.$id', '$.description', '$.oneOf[0].$ref', '$.oneOf[1].$ref', '$.oneOf[2].$ref', '$.oneOf[3].$ref', '$.$defs.outputUnit.properties.valid.type', '$.$defs.outputUnit.properties.keywordLocation.type', '$.$defs.outputUnit.properties.keywordLocation.format', '$.$defs.outputUnit.properties.absoluteKeywordLocation.type', '$.$defs.outputUnit.properties.absoluteKeywordLocation.format', '$.$defs.outputUnit.properties.instanceLocation.type', '$.$defs.outputUnit.properties.instanceLocation.format', '$.$defs.outputUnit.properties.errors.$ref', '$.$defs.outputUnit.properties.annotations.$ref', '$.$defs.outputUnit.required[0]', '$.$defs.outputUnit.required[1]', '$.$defs.outputUnit.required[2]', '$.$defs.outputUnit.allOf[0].if.properties.valid.const', '$.$defs.outputUnit.allOf[0].then.required[0]', '$.$defs.outputUnit.allOf[1].if.oneOf[0].properties.keywordLocation.pattern', '$.$defs.outputUnit.allOf[1].if.oneOf[1].properties.keywordLocation.pattern', '$.$defs.outputUnit.allOf[1].then.required[0]', '$.$defs.outputUnitArray.type', '$.$defs.outputUnitArray.items.$ref', '$.$defs.flag.properties.valid.type', '$.$defs.flag.required[0]', '$.$defs.basic.$ref', '$.$defs.detailed.$ref', '$.$defs.verbose.$ref'],
        ['https://json-schema.org/draft/2019-09/schema', 'https://json-schema.org/draft/2019-09/output/schema', 'A schema that validates the minimum requirements for validation output', '#/$defs/flag', '#/$defs/basic', '#/$defs/detailed', '#/$defs/verbose', 'boolean', 'string', 'uri-reference', 'string', 'uri', 'string', 'uri-reference', '#/$defs/outputUnitArray', '#/$defs/outputUnitArray', 'valid', 'keywordLocation', 'instanceLocation', False, 'errors', '.*/$ref/.*', '.*/$recursiveRef/.*', 'absoluteKeywordLocation', 'array', '#/$defs/outputUnit', 'boolean', 'valid', '#/outputUnit', '#/outputUnit', '#/outputUnit']
    ),
    (
        {'@context': 'https://schema.org/', '@type': 'Dataset', 'name': 'NCDC Storm Events Database', 'description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', 'url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', 'sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', 'identifier': ['https://doi.org/10.1000/182', 'https://identifiers.org/ark:/12345/fk1234'], 'keywords': ['ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE'], 'creator': {'@type': 'Organization', 'url': 'https://www.ncei.noaa.gov/', 'name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', 'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+1-828-271-4800', 'email': 'ncei.orders@noaa.gov'}}, 'includedInDataCatalog': {'@type': 'DataCatalog', 'name': 'data.gov'}, 'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'CSV', 'contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp'}, {'@type': 'DataDownload', 'encodingFormat': 'XML', 'contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510'}], 'temporalCoverage': '1950-01-01/2013-12-18', 'spatialCoverage': {'@type': 'Place', 'geo': {'@type': 'GeoShape', 'box': '18.0 -65.0 72.0 172.0'}}},
        ['$.@context', '$.@type', '$.name', '$.description', '$.url', '$.sameAs', '$.identifier[0]', '$.identifier[1]', '$.keywords[0]', '$.keywords[1]', '$.keywords[2]', '$.keywords[3]', '$.creator.@type', '$.creator.url', '$.creator.name', '$.creator.contactPoint.@type', '$.creator.contactPoint.contactType', '$.creator.contactPoint.telephone', '$.creator.contactPoint.email', '$.includedInDataCatalog.@type', '$.includedInDataCatalog.name', '$.distribution[0].@type', '$.distribution[0].encodingFormat', '$.distribution[0].contentUrl', '$.distribution[1].@type', '$.distribution[1].encodingFormat', '$.distribution[1].contentUrl', '$.temporalCoverage', '$.spatialCoverage.@type', '$.spatialCoverage.geo.@type', '$.spatialCoverage.geo.box'],
        ['https://schema.org/', 'Dataset', 'NCDC Storm Events Database', 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', 'https://catalog.data.gov/dataset/ncdc-storm-events-database', 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', 'https://doi.org/10.1000/182', 'https://identifiers.org/ark:/12345/fk1234', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE', 'Organization', 'https://www.ncei.noaa.gov/', 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', 'ContactPoint', 'customer service', '+1-828-271-4800', 'ncei.orders@noaa.gov', 'DataCatalog', 'data.gov', 'DataDownload', 'CSV', 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp', 'DataDownload', 'XML', 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', '1950-01-01/2013-12-18', 'Place', 'GeoShape', '18.0 -65.0 72.0 172.0']
    )
])
def test_listAllValues(json, paths, output):
    app = JSON2Flat()
    values = app.listAllValues(json, paths)
    print(values)
    assert output == values

@pytest.mark.parametrize('input,output', [
    (
        {'id': 1, 'name':'john doe'},
        {'$.id': 1,'$.name':'john doe'}
    ),
    (
        {'$schema': 'https://json-schema.org/draft/2019-09/schema', '$id': 'https://json-schema.org/draft/2019-09/output/schema', 'description': 'A schema that validates the minimum requirements for validation output', 'oneOf': [{'$ref': '#/$defs/flag'}, {'$ref': '#/$defs/basic'}, {'$ref': '#/$defs/detailed'}, {'$ref': '#/$defs/verbose'}], '$defs': {'outputUnit': {'properties': {'valid': {'type': 'boolean'}, 'keywordLocation': {'type': 'string', 'format': 'uri-reference'}, 'absoluteKeywordLocation': {'type': 'string', 'format': 'uri'}, 'instanceLocation': {'type': 'string', 'format': 'uri-reference'}, 'errors': {'$ref': '#/$defs/outputUnitArray'}, 'annotations': {'$ref': '#/$defs/outputUnitArray'}}, 'required': ['valid', 'keywordLocation', 'instanceLocation'], 'allOf': [{'if': {'properties': {'valid': {'const': False}}}, 'then': {'required': ['errors']}}, {'if': {'oneOf': [{'properties': {'keywordLocation': {'pattern': '.*/$ref/.*'}}}, {'properties': {'keywordLocation': {'pattern': '.*/$recursiveRef/.*'}}}]}, 'then': {'required': ['absoluteKeywordLocation']}}]}, 'outputUnitArray': {'type': 'array', 'items': {'$ref': '#/$defs/outputUnit'}}, 'flag': {'properties': {'valid': {'type': 'boolean'}}, 'required': ['valid']}, 'basic': {'$ref': '#/outputUnit'}, 'detailed': {'$ref': '#/outputUnit'}, 'verbose': {'$ref': '#/outputUnit'}}},
        {'$.$schema': 'https://json-schema.org/draft/2019-09/schema', '$.$id': 'https://json-schema.org/draft/2019-09/output/schema', '$.description': 'A schema that validates the minimum requirements for validation output', '$.oneOf[0].$ref': '#/$defs/flag', '$.oneOf[1].$ref': '#/$defs/basic', '$.oneOf[2].$ref': '#/$defs/detailed', '$.oneOf[3].$ref': '#/$defs/verbose', '$.$defs.outputUnit.properties.valid.type': 'boolean', '$.$defs.outputUnit.properties.keywordLocation.type': 'string', '$.$defs.outputUnit.properties.keywordLocation.format': 'uri-reference', '$.$defs.outputUnit.properties.absoluteKeywordLocation.type': 'string', '$.$defs.outputUnit.properties.absoluteKeywordLocation.format': 'uri', '$.$defs.outputUnit.properties.instanceLocation.type': 'string', '$.$defs.outputUnit.properties.instanceLocation.format': 'uri-reference', '$.$defs.outputUnit.properties.errors.$ref': '#/$defs/outputUnitArray', '$.$defs.outputUnit.properties.annotations.$ref': '#/$defs/outputUnitArray', '$.$defs.outputUnit.required[0]': 'valid', '$.$defs.outputUnit.required[1]': 'keywordLocation', '$.$defs.outputUnit.required[2]': 'instanceLocation', '$.$defs.outputUnit.allOf[0].if.properties.valid.const': False, '$.$defs.outputUnit.allOf[0].then.required[0]': 'errors', '$.$defs.outputUnit.allOf[1].if.oneOf[0].properties.keywordLocation.pattern': '.*/$ref/.*', '$.$defs.outputUnit.allOf[1].if.oneOf[1].properties.keywordLocation.pattern': '.*/$recursiveRef/.*', '$.$defs.outputUnit.allOf[1].then.required[0]': 'absoluteKeywordLocation', '$.$defs.outputUnitArray.type': 'array', '$.$defs.outputUnitArray.items.$ref': '#/$defs/outputUnit', '$.$defs.flag.properties.valid.type': 'boolean', '$.$defs.flag.required[0]': 'valid', '$.$defs.basic.$ref': '#/outputUnit', '$.$defs.detailed.$ref': '#/outputUnit', '$.$defs.verbose.$ref': '#/outputUnit'}
    ),
    (
        {'@context': 'https://schema.org/', '@type': 'Dataset', 'name': 'NCDC Storm Events Database', 'description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', 'url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', 'sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', 'identifier': ['https://doi.org/10.1000/182', 'https://identifiers.org/ark:/12345/fk1234'], 'keywords': ['ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE'], 'creator': {'@type': 'Organization', 'url': 'https://www.ncei.noaa.gov/', 'name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', 'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+1-828-271-4800', 'email': 'ncei.orders@noaa.gov'}}, 'includedInDataCatalog': {'@type': 'DataCatalog', 'name': 'data.gov'}, 'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'CSV', 'contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp'}, {'@type': 'DataDownload', 'encodingFormat': 'XML', 'contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510'}], 'temporalCoverage': '1950-01-01/2013-12-18', 'spatialCoverage': {'@type': 'Place', 'geo': {'@type': 'GeoShape', 'box': '18.0 -65.0 72.0 172.0'}}},
        {'$.@context': 'https://schema.org/', '$.@type': 'Dataset', '$.name': 'NCDC Storm Events Database', '$.description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', '$.url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', '$.sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', '$.identifier[0]': 'https://doi.org/10.1000/182', '$.identifier[1]': 'https://identifiers.org/ark:/12345/fk1234', '$.keywords[0]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', '$.keywords[1]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', '$.keywords[2]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', '$.keywords[3]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE', '$.creator.@type': 'Organization', '$.creator.url': 'https://www.ncei.noaa.gov/', '$.creator.name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', '$.creator.contactPoint.@type': 'ContactPoint', '$.creator.contactPoint.contactType': 'customer service', '$.creator.contactPoint.telephone': '+1-828-271-4800', '$.creator.contactPoint.email': 'ncei.orders@noaa.gov', '$.includedInDataCatalog.@type': 'DataCatalog', '$.includedInDataCatalog.name': 'data.gov', '$.distribution[0].@type': 'DataDownload', '$.distribution[0].encodingFormat': 'CSV', '$.distribution[0].contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp', '$.distribution[1].@type': 'DataDownload', '$.distribution[1].encodingFormat': 'XML', '$.distribution[1].contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', '$.temporalCoverage': '1950-01-01/2013-12-18', '$.spatialCoverage.@type': 'Place', '$.spatialCoverage.geo.@type': 'GeoShape', '$.spatialCoverage.geo.box': '18.0 -65.0 72.0 172.0'}
    )
 ])
def test_toFlat(input, output):
    app = JSON2Flat()
    values = app.toFlat(input)
    assert output == values

@pytest.mark.parametrize('input,output', [
    (
        {'$.id': 1,'$.name':'john doe'},
        {'id': 1, 'name':'john doe'}
    ),
    (
        {'$.$schema': 'https://json-schema.org/draft/2019-09/schema', '$.$id': 'https://json-schema.org/draft/2019-09/output/schema', '$.description': 'A schema that validates the minimum requirements for validation output', '$.oneOf[0].$ref': '#/$defs/flag', '$.oneOf[1].$ref': '#/$defs/basic', '$.oneOf[2].$ref': '#/$defs/detailed', '$.oneOf[3].$ref': '#/$defs/verbose', '$.$defs.outputUnit.properties.valid.type': 'boolean', '$.$defs.outputUnit.properties.keywordLocation.type': 'string', '$.$defs.outputUnit.properties.keywordLocation.format': 'uri-reference', '$.$defs.outputUnit.properties.absoluteKeywordLocation.type': 'string', '$.$defs.outputUnit.properties.absoluteKeywordLocation.format': 'uri', '$.$defs.outputUnit.properties.instanceLocation.type': 'string', '$.$defs.outputUnit.properties.instanceLocation.format': 'uri-reference', '$.$defs.outputUnit.properties.errors.$ref': '#/$defs/outputUnitArray', '$.$defs.outputUnit.properties.annotations.$ref': '#/$defs/outputUnitArray', '$.$defs.outputUnit.required[0]': 'valid', '$.$defs.outputUnit.required[1]': 'keywordLocation', '$.$defs.outputUnit.required[2]': 'instanceLocation', '$.$defs.outputUnit.allOf[0].if.properties.valid.const': False, '$.$defs.outputUnit.allOf[0].then.required[0]': 'errors', '$.$defs.outputUnit.allOf[1].if.oneOf[0].properties.keywordLocation.pattern': '.*/$ref/.*', '$.$defs.outputUnit.allOf[1].if.oneOf[1].properties.keywordLocation.pattern': '.*/$recursiveRef/.*', '$.$defs.outputUnit.allOf[1].then.required[0]': 'absoluteKeywordLocation', '$.$defs.outputUnitArray.type': 'array', '$.$defs.outputUnitArray.items.$ref': '#/$defs/outputUnit', '$.$defs.flag.properties.valid.type': 'boolean', '$.$defs.flag.required[0]': 'valid', '$.$defs.basic.$ref': '#/outputUnit', '$.$defs.detailed.$ref': '#/outputUnit', '$.$defs.verbose.$ref': '#/outputUnit'},
        {'$schema': 'https://json-schema.org/draft/2019-09/schema', '$id': 'https://json-schema.org/draft/2019-09/output/schema', 'description': 'A schema that validates the minimum requirements for validation output', 'oneOf': [{'$ref': '#/$defs/flag'}, {'$ref': '#/$defs/basic'}, {'$ref': '#/$defs/detailed'}, {'$ref': '#/$defs/verbose'}], '$defs': {'outputUnit': {'properties': {'valid': {'type': 'boolean'}, 'keywordLocation': {'type': 'string', 'format': 'uri-reference'}, 'absoluteKeywordLocation': {'type': 'string', 'format': 'uri'}, 'instanceLocation': {'type': 'string', 'format': 'uri-reference'}, 'errors': {'$ref': '#/$defs/outputUnitArray'}, 'annotations': {'$ref': '#/$defs/outputUnitArray'}}, 'required': ['valid', 'keywordLocation', 'instanceLocation'], 'allOf': [{'if': {'properties': {'valid': {'const': False}}}, 'then': {'required': ['errors']}}, {'if': {'oneOf': [{'properties': {'keywordLocation': {'pattern': '.*/$ref/.*'}}}, {'properties': {'keywordLocation': {'pattern': '.*/$recursiveRef/.*'}}}]}, 'then': {'required': ['absoluteKeywordLocation']}}]}, 'outputUnitArray': {'type': 'array', 'items': {'$ref': '#/$defs/outputUnit'}}, 'flag': {'properties': {'valid': {'type': 'boolean'}}, 'required': ['valid']}, 'basic': {'$ref': '#/outputUnit'}, 'detailed': {'$ref': '#/outputUnit'}, 'verbose': {'$ref': '#/outputUnit'}}}
    ),
    (
        {'$.@context': 'https://schema.org/', '$.@type': 'Dataset', '$.name': 'NCDC Storm Events Database', '$.description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', '$.url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', '$.sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', '$.identifier[0]': 'https://doi.org/10.1000/182', '$.identifier[1]': 'https://identifiers.org/ark:/12345/fk1234', '$.keywords[0]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', '$.keywords[1]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', '$.keywords[2]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', '$.keywords[3]': 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE', '$.creator.@type': 'Organization', '$.creator.url': 'https://www.ncei.noaa.gov/', '$.creator.name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', '$.creator.contactPoint.@type': 'ContactPoint', '$.creator.contactPoint.contactType': 'customer service', '$.creator.contactPoint.telephone': '+1-828-271-4800', '$.creator.contactPoint.email': 'ncei.orders@noaa.gov', '$.includedInDataCatalog.@type': 'DataCatalog', '$.includedInDataCatalog.name': 'data.gov', '$.distribution[0].@type': 'DataDownload', '$.distribution[0].encodingFormat': 'CSV', '$.distribution[0].contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp', '$.distribution[1].@type': 'DataDownload', '$.distribution[1].encodingFormat': 'XML', '$.distribution[1].contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', '$.temporalCoverage': '1950-01-01/2013-12-18', '$.spatialCoverage.@type': 'Place', '$.spatialCoverage.geo.@type': 'GeoShape', '$.spatialCoverage.geo.box': '18.0 -65.0 72.0 172.0'},
        {'@context': 'https://schema.org/', '@type': 'Dataset', 'name': 'NCDC Storm Events Database', 'description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', 'url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', 'sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', 'identifier': ['https://doi.org/10.1000/182', 'https://identifiers.org/ark:/12345/fk1234'], 'keywords': ['ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE'], 'creator': {'@type': 'Organization', 'url': 'https://www.ncei.noaa.gov/', 'name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', 'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+1-828-271-4800', 'email': 'ncei.orders@noaa.gov'}}, 'includedInDataCatalog': {'@type': 'DataCatalog', 'name': 'data.gov'}, 'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'CSV', 'contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp'}, {'@type': 'DataDownload', 'encodingFormat': 'XML', 'contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510'}], 'temporalCoverage': '1950-01-01/2013-12-18', 'spatialCoverage': {'@type': 'Place', 'geo': {'@type': 'GeoShape', 'box': '18.0 -65.0 72.0 172.0'}}}
    )
])
def test_toStructure(input, output):
    app = JSON2Flat()
    values = app.toStructure(input)

    assert output == values


@pytest.mark.parametrize('input,output', [
    (
        [{'id': 1, 'name':'john doe'}],
        '"$.id","$.name"\r\n1,"john doe"\r\n'
    ),
    (
        [{'$schema': 'https://json-schema.org/draft/2019-09/schema', '$id': 'https://json-schema.org/draft/2019-09/output/schema', 'description': 'A schema that validates the minimum requirements for validation output', 'oneOf': [{'$ref': '#/$defs/flag'}, {'$ref': '#/$defs/basic'}, {'$ref': '#/$defs/detailed'}, {'$ref': '#/$defs/verbose'}], '$defs': {'outputUnit': {'properties': {'valid': {'type': 'boolean'}, 'keywordLocation': {'type': 'string', 'format': 'uri-reference'}, 'absoluteKeywordLocation': {'type': 'string', 'format': 'uri'}, 'instanceLocation': {'type': 'string', 'format': 'uri-reference'}, 'errors': {'$ref': '#/$defs/outputUnitArray'}, 'annotations': {'$ref': '#/$defs/outputUnitArray'}}, 'required': ['valid', 'keywordLocation', 'instanceLocation'], 'allOf': [{'if': {'properties': {'valid': {'const': False}}}, 'then': {'required': ['errors']}}, {'if': {'oneOf': [{'properties': {'keywordLocation': {'pattern': '.*/$ref/.*'}}}, {'properties': {'keywordLocation': {'pattern': '.*/$recursiveRef/.*'}}}]}, 'then': {'required': ['absoluteKeywordLocation']}}]}, 'outputUnitArray': {'type': 'array', 'items': {'$ref': '#/$defs/outputUnit'}}, 'flag': {'properties': {'valid': {'type': 'boolean'}}, 'required': ['valid']}, 'basic': {'$ref': '#/outputUnit'}, 'detailed': {'$ref': '#/outputUnit'}, 'verbose': {'$ref': '#/outputUnit'}}}],
        '"$.$schema","$.$id","$.description","$.oneOf[0].$ref","$.oneOf[1].$ref","$.oneOf[2].$ref","$.oneOf[3].$ref","$.$defs.outputUnit.properties.valid.type","$.$defs.outputUnit.properties.keywordLocation.type","$.$defs.outputUnit.properties.keywordLocation.format","$.$defs.outputUnit.properties.absoluteKeywordLocation.type","$.$defs.outputUnit.properties.absoluteKeywordLocation.format","$.$defs.outputUnit.properties.instanceLocation.type","$.$defs.outputUnit.properties.instanceLocation.format","$.$defs.outputUnit.properties.errors.$ref","$.$defs.outputUnit.properties.annotations.$ref","$.$defs.outputUnit.required[0]","$.$defs.outputUnit.required[1]","$.$defs.outputUnit.required[2]","$.$defs.outputUnit.allOf[0].if.properties.valid.const","$.$defs.outputUnit.allOf[0].then.required[0]","$.$defs.outputUnit.allOf[1].if.oneOf[0].properties.keywordLocation.pattern","$.$defs.outputUnit.allOf[1].if.oneOf[1].properties.keywordLocation.pattern","$.$defs.outputUnit.allOf[1].then.required[0]","$.$defs.outputUnitArray.type","$.$defs.outputUnitArray.items.$ref","$.$defs.flag.properties.valid.type","$.$defs.flag.required[0]","$.$defs.basic.$ref","$.$defs.detailed.$ref","$.$defs.verbose.$ref"\r\n"https://json-schema.org/draft/2019-09/schema","https://json-schema.org/draft/2019-09/output/schema","A schema that validates the minimum requirements for validation output","#/$defs/flag","#/$defs/basic","#/$defs/detailed","#/$defs/verbose","boolean","string","uri-reference","string","uri","string","uri-reference","#/$defs/outputUnitArray","#/$defs/outputUnitArray","valid","keywordLocation","instanceLocation",False,"errors",".*/$ref/.*",".*/$recursiveRef/.*","absoluteKeywordLocation","array","#/$defs/outputUnit","boolean","valid","#/outputUnit","#/outputUnit","#/outputUnit"\r\n'
    ),
    (
        [{'@context': 'https://schema.org/', '@type': 'Dataset', 'name': 'NCDC Storm Events Database', 'description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', 'url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', 'sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', 'identifier': ['https://doi.org/10.1000/182', 'https://identifiers.org/ark:/12345/fk1234'], 'keywords': ['ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE'], 'creator': {'@type': 'Organization', 'url': 'https://www.ncei.noaa.gov/', 'name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', 'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+1-828-271-4800', 'email': 'ncei.orders@noaa.gov'}}, 'includedInDataCatalog': {'@type': 'DataCatalog', 'name': 'data.gov'}, 'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'CSV', 'contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp'}, {'@type': 'DataDownload', 'encodingFormat': 'XML', 'contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510'}], 'temporalCoverage': '1950-01-01/2013-12-18', 'spatialCoverage': {'@type': 'Place', 'geo': {'@type': 'GeoShape', 'box': '18.0 -65.0 72.0 172.0'}}}],
        '"$.@context","$.@type","$.name","$.description","$.url","$.sameAs","$.identifier[0]","$.identifier[1]","$.keywords[0]","$.keywords[1]","$.keywords[2]","$.keywords[3]","$.creator.@type","$.creator.url","$.creator.name","$.creator.contactPoint.@type","$.creator.contactPoint.contactType","$.creator.contactPoint.telephone","$.creator.contactPoint.email","$.includedInDataCatalog.@type","$.includedInDataCatalog.name","$.distribution[0].@type","$.distribution[0].encodingFormat","$.distribution[0].contentUrl","$.distribution[1].@type","$.distribution[1].encodingFormat","$.distribution[1].contentUrl","$.temporalCoverage","$.spatialCoverage.@type","$.spatialCoverage.geo.@type","$.spatialCoverage.geo.box"\r\n"https://schema.org/","Dataset","NCDC Storm Events Database","Storm Data is provided by the National Weather Service (NWS) and contain statistics on...","https://catalog.data.gov/dataset/ncdc-storm-events-database","https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510","https://doi.org/10.1000/182","https://identifiers.org/ark:/12345/fk1234","ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES","ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT","ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG","ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE","Organization","https://www.ncei.noaa.gov/","OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce","ContactPoint","customer service","+1-828-271-4800","ncei.orders@noaa.gov","DataCatalog","data.gov","DataDownload","CSV","http://www.ncdc.noaa.gov/stormevents/ftp.jsp","DataDownload","XML","http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510","1950-01-01/2013-12-18","Place","GeoShape","18.0 -65.0 72.0 172.0"\r\n'
    )
])
def test_writeCSV(input,output):
    app = JSON2CSV()
    file =  io.StringIO()
    app.writeCSV(input,file)
    values = file.getvalue()
    assert output == values

@pytest.mark.parametrize('input,output', [
    (
        '"$.id","$.name"\r\n1,"john doe"\r\n',
        [{'id': 1, 'name':'john doe'}]
    ),
    (
        '"$.$schema","$.$id","$.description","$.oneOf[0].$ref","$.oneOf[1].$ref","$.oneOf[2].$ref","$.oneOf[3].$ref","$.$defs.outputUnit.properties.valid.type","$.$defs.outputUnit.properties.keywordLocation.type","$.$defs.outputUnit.properties.keywordLocation.format","$.$defs.outputUnit.properties.absoluteKeywordLocation.type","$.$defs.outputUnit.properties.absoluteKeywordLocation.format","$.$defs.outputUnit.properties.instanceLocation.type","$.$defs.outputUnit.properties.instanceLocation.format","$.$defs.outputUnit.properties.errors.$ref","$.$defs.outputUnit.properties.annotations.$ref","$.$defs.outputUnit.required[0]","$.$defs.outputUnit.required[1]","$.$defs.outputUnit.required[2]","$.$defs.outputUnit.allOf[0].if.properties.valid.const","$.$defs.outputUnit.allOf[0].then.required[0]","$.$defs.outputUnit.allOf[1].if.oneOf[0].properties.keywordLocation.pattern","$.$defs.outputUnit.allOf[1].if.oneOf[1].properties.keywordLocation.pattern","$.$defs.outputUnit.allOf[1].then.required[0]","$.$defs.outputUnitArray.type","$.$defs.outputUnitArray.items.$ref","$.$defs.flag.properties.valid.type","$.$defs.flag.required[0]","$.$defs.basic.$ref","$.$defs.detailed.$ref","$.$defs.verbose.$ref"\r\n"https://json-schema.org/draft/2019-09/schema","https://json-schema.org/draft/2019-09/output/schema","A schema that validates the minimum requirements for validation output","#/$defs/flag","#/$defs/basic","#/$defs/detailed","#/$defs/verbose","boolean","string","uri-reference","string","uri","string","uri-reference","#/$defs/outputUnitArray","#/$defs/outputUnitArray","valid","keywordLocation","instanceLocation",False,"errors",".*/$ref/.*",".*/$recursiveRef/.*","absoluteKeywordLocation","array","#/$defs/outputUnit","boolean","valid","#/outputUnit","#/outputUnit","#/outputUnit"\r\n',
        [{'$schema': 'https://json-schema.org/draft/2019-09/schema', '$id': 'https://json-schema.org/draft/2019-09/output/schema', 'description': 'A schema that validates the minimum requirements for validation output', 'oneOf': [{'$ref': '#/$defs/flag'}, {'$ref': '#/$defs/basic'}, {'$ref': '#/$defs/detailed'}, {'$ref': '#/$defs/verbose'}], '$defs': {'outputUnit': {'properties': {'valid': {'type': 'boolean'}, 'keywordLocation': {'type': 'string', 'format': 'uri-reference'}, 'absoluteKeywordLocation': {'type': 'string', 'format': 'uri'}, 'instanceLocation': {'type': 'string', 'format': 'uri-reference'}, 'errors': {'$ref': '#/$defs/outputUnitArray'}, 'annotations': {'$ref': '#/$defs/outputUnitArray'}}, 'required': ['valid', 'keywordLocation', 'instanceLocation'], 'allOf': [{'if': {'properties': {'valid': {'const': False}}}, 'then': {'required': ['errors']}}, {'if': {'oneOf': [{'properties': {'keywordLocation': {'pattern': '.*/$ref/.*'}}}, {'properties': {'keywordLocation': {'pattern': '.*/$recursiveRef/.*'}}}]}, 'then': {'required': ['absoluteKeywordLocation']}}]}, 'outputUnitArray': {'type': 'array', 'items': {'$ref': '#/$defs/outputUnit'}}, 'flag': {'properties': {'valid': {'type': 'boolean'}}, 'required': ['valid']}, 'basic': {'$ref': '#/outputUnit'}, 'detailed': {'$ref': '#/outputUnit'}, 'verbose': {'$ref': '#/outputUnit'}}}]
    ),
    (
        '"$.@context","$.@type","$.name","$.description","$.url","$.sameAs","$.identifier[0]","$.identifier[1]","$.keywords[0]","$.keywords[1]","$.keywords[2]","$.keywords[3]","$.creator.@type","$.creator.url","$.creator.name","$.creator.contactPoint.@type","$.creator.contactPoint.contactType","$.creator.contactPoint.telephone","$.creator.contactPoint.email","$.includedInDataCatalog.@type","$.includedInDataCatalog.name","$.distribution[0].@type","$.distribution[0].encodingFormat","$.distribution[0].contentUrl","$.distribution[1].@type","$.distribution[1].encodingFormat","$.distribution[1].contentUrl","$.temporalCoverage","$.spatialCoverage.@type","$.spatialCoverage.geo.@type","$.spatialCoverage.geo.box"\r\n"https://schema.org/","Dataset","NCDC Storm Events Database","Storm Data is provided by the National Weather Service (NWS) and contain statistics on...","https://catalog.data.gov/dataset/ncdc-storm-events-database","https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510","https://doi.org/10.1000/182","https://identifiers.org/ark:/12345/fk1234","ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES","ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT","ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG","ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE","Organization","https://www.ncei.noaa.gov/","OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce","ContactPoint","customer service","+1-828-271-4800","ncei.orders@noaa.gov","DataCatalog","data.gov","DataDownload","CSV","http://www.ncdc.noaa.gov/stormevents/ftp.jsp","DataDownload","XML","http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510","1950-01-01/2013-12-18","Place","GeoShape","18.0 -65.0 72.0 172.0"\r\n',
        [{'@context': 'https://schema.org/', '@type': 'Dataset', 'name': 'NCDC Storm Events Database', 'description': 'Storm Data is provided by the National Weather Service (NWS) and contain statistics on...', 'url': 'https://catalog.data.gov/dataset/ncdc-storm-events-database', 'sameAs': 'https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510', 'identifier': ['https://doi.org/10.1000/182', 'https://identifiers.org/ark:/12345/fk1234'], 'keywords': ['ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG', 'ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE'], 'creator': {'@type': 'Organization', 'url': 'https://www.ncei.noaa.gov/', 'name': 'OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce', 'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+1-828-271-4800', 'email': 'ncei.orders@noaa.gov'}}, 'includedInDataCatalog': {'@type': 'DataCatalog', 'name': 'data.gov'}, 'distribution': [{'@type': 'DataDownload', 'encodingFormat': 'CSV', 'contentUrl': 'http://www.ncdc.noaa.gov/stormevents/ftp.jsp'}, {'@type': 'DataDownload', 'encodingFormat': 'XML', 'contentUrl': 'http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510'}], 'temporalCoverage': '1950-01-01/2013-12-18', 'spatialCoverage': {'@type': 'Place', 'geo': {'@type': 'GeoShape', 'box': '18.0 -65.0 72.0 172.0'}}}]
    )
])
def test_readCSV(input,output):
    app = JSON2CSV()
    file =  io.StringIO(input)
    values = app.readCSV(file)
    assert output == values