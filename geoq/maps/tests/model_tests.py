import sys
import datetime
import json
from django.test import TestCase
from geoq.maps.models import *

class BaseTest(TestCase):
    
    TestCase.maxDiff = None
    
#    def setUp(self):
#        comment_user = User.objects.get(id=4)
#        comment_aoi = AOI.objects.get(id=6508) #for testLog function
#        Comment.objects.create(user=comment_user, aoi=comment_aoi, text="Test Log") # for testLogJSON and testToDic functions
#        Organization.objects.create(name="MITRE", url="www.mitre.org")
    

class LayerTest(BaseTest):
        
    def testUnicode(self):
        """ -- Verify Layer name returnd by __unicode__ function."""
        layer = Layer.objects.get(id=1)
        self.assertEqual(unicode(layer), "Nexrad")
        
    def testGetLayerUrls(self):
        """ -- Verify layer url list of project"""
        layer = Layer.objects.get(id=1)
        urls = layer.get_layer_urls()
        self.assertEqual(urls, [])
        
    def testGetAbsoluteUrl(self):
        """ -- Verify Layer absolute url."""
        layer = Layer.objects.get(id=1)
        url = layer.get_absolute_url()
        self.assertEqual(url, "/maps/layers/update/1")
        
    def testGetLayerParams(self):
        """ -- Verify Layer params."""
        layer = Layer.objects.get(id=1)
        params = layer.get_layer_params()
        self.assertEqual(params, {})
        
    def testLayerJson(self):
        """ -- Verify Layer using JSON format."""
        layer = Layer.objects.get(id=1)
        json = layer.layer_json()
        self.assertEqual(json, {'attribution': u'Weather data \xa9 2012 IEM Nexrad',
                                 'description': u'',
                                 'downloadableLink': u'',
                                 'dynamicParams': None,
                                 'enableIdentify': False,
                                 'fieldsToShow': u'',
                                 'format': u'image/png',
                                 'id': 1,
                                 'infoFormat': None,
                                 'layer': u'nexrad-n0r-900913',
                                 'layerParams': {},
                                 'layerParsingFunction': None,
                                 'layer_info_link': None,
                                 'name': u'Nexrad',
                                 'refreshrate': None,
                                 'rootField': u'',
                                 'spatialReference': u'EPSG:4326',
                                 'styles': u'',
                                 'subdomains': [],
                                 'token': u'',
                                 'transparent': True,
                                 'type': u'WMS',
                                 'url': u'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi'})
    
class MapTest(BaseTest):
    
    def testUnicode(self):
        """ -- Verify Map name returnd by __unicode__ function."""
        map = Map.objects.get(id=1)
        self.assertEqual(unicode(map), "Base Map")
    
    def testName(self):
        """ -- Verify Map name returnd by name function."""
        map = Map.objects.get(id=1)
        self.assertEqual(map.name, "Base Map")
        
    def testCenter(self):
        """ -- Verify the center (center_x, center_y) of a Map."""
        map = Map.objects.get(id=1)
        self.assertEqual(map.center, (0.0, 0.0))
        
    def testLayers(self):
        """ -- Verify Layers of a Map."""
        map = Map.objects.get(id=1)
        layers = map.layers
        self.assertEqual(len(layers), 2)
        
    def testMapLayersJson(self):
        """ -- Verify Layers of a Map using JSON format."""
        map = Map.objects.get(id=1)
        json = map.map_layers_json()
        self.assertEqual(len(json), 2)
        self.assertEqual(json, [{'styles': u'',
                                 'layer': u'nexrad-n0r-900913',
                                 'enableIdentify': False,
                                 'layer_info_link': None,
                                 'downloadableLink': u'',
                                 'spatialReference': u'EPSG:4326',
                                 'id': 1,
                                 'maplayer_id': 1,
                                 'shown': True,
                                 'layerParsingFunction': None,
                                 'rootField': u'',
                                 'type': u'WMS',
                                 'infoFormat': None,
                                 'opacity': 0.8,
                                 'dynamicParams': None,
                                 'attribution': u'Weather data \xa9 2012 IEM Nexrad',
                                 'description': u'',
                                 'format': u'image/png',
                                 'fieldsToShow': u'',
                                 'zIndex': 0,
                                 'layerParams': {},
                                 'transparent': True,
                                 'refreshrate': None,
                                 'isBaseLayer': False,
                                 'name': u'Nexrad',
                                 'url': u'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi',
                                 'subdomains': [],
                                 'displayInLayerSwitcher': False,
                                 'token': u''},
                                {'styles': u'',
                                 'layer': u'',
                                 'enableIdentify': False,
                                 'layer_info_link': None,
                                 'downloadableLink': u'',
                                 'spatialReference': u'EPSG:4326',
                                 'id': 3,
                                 'maplayer_id': 2,
                                 'shown': True,
                                 'layerParsingFunction': None,
                                 'rootField': u'',
                                 'type': u'WMS',
                                 'infoFormat': None,
                                 'opacity': 0.8,
                                 'dynamicParams': None,
                                 'attribution': u'',
                                 'description': u'',
                                 'format': u'png24',
                                 'fieldsToShow': u'',
                                 'zIndex': 1,
                                 'layerParams': {u'dpi': 92, u'f': u'image'},
                                 'transparent': True,
                                 'refreshrate': None,
                                 'isBaseLayer': False,
                                 'name': u'National Map',
                                 'url': u'http://raster.nationalmap.gov/ArcGIS/rest/services/TNM_Large_Scale_Imagery/MapServer/export',
                                 'subdomains': [],
                                 'displayInLayerSwitcher': False,
                                 'token': u''}])
        
    def testAllMapLayersJson(self):
        """ -- Verify all Layers enabled using JSON format."""
        map = Map.objects.get(id=1)
        json = map.all_map_layers_json()
        self.assertEqual(json, '[{"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 5, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "GeoJSON", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": null, "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "Chicago Zip Codes", "url": "https://raw.github.com/smartchicago/chicago-atlas/master/db/import/zipcodes.geojson", "subdomains": [], "token": ""}, {"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 6, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "GeoJSON", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": null, "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "DC Bars", "url": "https://raw.github.com/benbalter/dc-wifi-social/master/bars.geojson", "subdomains": [], "token": ""}, {"layer": "AIRS_Precipitation_Day", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 7, "dynamicParams": [{"range": {"start": "2012-05-08", "type": "FixedRange"}, "type": "Date", "name": "Time"}], "layerParsingFunction": null, "rootField": "", "type": "WMTS", "infoFormat": null, "styles": "", "attribution": "", "description": "NASA Satellite", "format": "jpeg", "fieldsToShow": "", "layerParams": {"layer": "AIRS_Precipitation_Day", "TileMatrixSet": "GoogleMapsCompatible_Level6", "Time": "2014-11-04"}, "transparent": true, "refreshrate": null, "name": "NASA AIRS Precipitation Day", "url": "http://map1.vis.earthdata.nasa.gov/wmts-webmerc/AIRS_Precipitation_Day/default/{Time}/{TileMatrixSet}/{z}/{y}/{x}.png", "subdomains": [], "token": ""}, {"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 3, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "WMS", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": "png24", "fieldsToShow": "", "layerParams": {"dpi": 92, "f": "image"}, "transparent": true, "refreshrate": null, "name": "National Map", "url": "http://raster.nationalmap.gov/ArcGIS/rest/services/TNM_Large_Scale_Imagery/MapServer/export", "subdomains": [], "token": ""}, {"layer": "nexrad-n0r-900913", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 1, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "WMS", "infoFormat": null, "styles": "", "attribution": "Weather data \\u00a9 2012 IEM Nexrad", "description": "", "format": "image/png", "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "Nexrad", "url": "http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi", "subdomains": [], "token": ""}, {"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 2, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "ArcGIS Tiled Map Service", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": null, "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "USA_Median_Household_Income", "url": "http://server.arcgisonline.com/ArcGIS/rest/services/Demographics/USA_Median_Household_Income/MapServer", "subdomains": [], "token": ""}]')
 
    def testToObject(self):
        """ -- Verify Map object """
        map = Map.objects.get(id=1)
        obj = map.to_object()
        self.assertEqual(obj, {'layers': [{'styles': u'', 'layer': u'nexrad-n0r-900913', 'enableIdentify': False, 'layer_info_link': None, 'downloadableLink': u'', 'spatialReference': u'EPSG:4326', 'id': 1, 'maplayer_id': 1, 'shown': True, 'layerParsingFunction': None, 'rootField': u'', 'type': u'WMS', 'infoFormat': None, 'opacity': 0.8, 'dynamicParams': None, 'attribution': u'Weather data \xa9 2012 IEM Nexrad', 'description': u'', 'format': u'image/png', 'fieldsToShow': u'', 'zIndex': 0, 'layerParams': {}, 'transparent': True, 'refreshrate': None, 'isBaseLayer': False, 'name': u'Nexrad', 'url': u'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi', 'subdomains': [], 'displayInLayerSwitcher': False, 'token': u''}, {'styles': u'', 'layer': u'', 'enableIdentify': False, 'layer_info_link': None, 'downloadableLink': u'', 'spatialReference': u'EPSG:4326', 'id': 3, 'maplayer_id': 2, 'shown': True, 'layerParsingFunction': None, 'rootField': u'', 'type': u'WMS', 'infoFormat': None, 'opacity': 0.8, 'dynamicParams': None, 'attribution': u'', 'description': u'', 'format': u'png24', 'fieldsToShow': u'', 'zIndex': 1, 'layerParams': {u'dpi': 92, u'f': u'image'}, 'transparent': True, 'refreshrate': None, 'isBaseLayer': False, 'name': u'National Map', 'url': u'http://raster.nationalmap.gov/ArcGIS/rest/services/TNM_Large_Scale_Imagery/MapServer/export', 'subdomains': [], 'displayInLayerSwitcher': False, 'token': u''}], 'projection': u'EPSG:4326', 'all_layers': '[{"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 5, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "GeoJSON", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": null, "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "Chicago Zip Codes", "url": "https://raw.github.com/smartchicago/chicago-atlas/master/db/import/zipcodes.geojson", "subdomains": [], "token": ""}, {"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 6, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "GeoJSON", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": null, "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "DC Bars", "url": "https://raw.github.com/benbalter/dc-wifi-social/master/bars.geojson", "subdomains": [], "token": ""}, {"layer": "AIRS_Precipitation_Day", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 7, "dynamicParams": [{"range": {"start": "2012-05-08", "type": "FixedRange"}, "type": "Date", "name": "Time"}], "layerParsingFunction": null, "rootField": "", "type": "WMTS", "infoFormat": null, "styles": "", "attribution": "", "description": "NASA Satellite", "format": "jpeg", "fieldsToShow": "", "layerParams": {"layer": "AIRS_Precipitation_Day", "TileMatrixSet": "GoogleMapsCompatible_Level6", "Time": "2014-11-04"}, "transparent": true, "refreshrate": null, "name": "NASA AIRS Precipitation Day", "url": "http://map1.vis.earthdata.nasa.gov/wmts-webmerc/AIRS_Precipitation_Day/default/{Time}/{TileMatrixSet}/{z}/{y}/{x}.png", "subdomains": [], "token": ""}, {"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 3, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "WMS", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": "png24", "fieldsToShow": "", "layerParams": {"dpi": 92, "f": "image"}, "transparent": true, "refreshrate": null, "name": "National Map", "url": "http://raster.nationalmap.gov/ArcGIS/rest/services/TNM_Large_Scale_Imagery/MapServer/export", "subdomains": [], "token": ""}, {"layer": "nexrad-n0r-900913", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 1, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "WMS", "infoFormat": null, "styles": "", "attribution": "Weather data \\u00a9 2012 IEM Nexrad", "description": "", "format": "image/png", "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "Nexrad", "url": "http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi", "subdomains": [], "token": ""}, {"layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 2, "dynamicParams": null, "layerParsingFunction": null, "rootField": "", "type": "ArcGIS Tiled Map Service", "infoFormat": null, "styles": "", "attribution": "", "description": "", "format": null, "fieldsToShow": "", "layerParams": {}, "transparent": true, "refreshrate": null, "name": "USA_Median_Household_Income", "url": "http://server.arcgisonline.com/ArcGIS/rest/services/Demographics/USA_Median_Household_Income/MapServer", "subdomains": [], "token": ""}]', 'zoom': 15, 'center_x': 0, 'center_y': 0})
        
    def testToJson(self):
        """ -- Verify Map using JSON format"""
        map = Map.objects.get(id=1)
        json = map.to_json()
        self.assertEqual(json, '{"layers": [{"styles": "", "layer": "nexrad-n0r-900913", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 1, "maplayer_id": 1, "shown": true, "layerParsingFunction": null, "rootField": "", "type": "WMS", "infoFormat": null, "opacity": 0.8, "dynamicParams": null, "attribution": "Weather data \\u00a9 2012 IEM Nexrad", "description": "", "format": "image/png", "fieldsToShow": "", "zIndex": 0, "layerParams": {}, "transparent": true, "refreshrate": null, "isBaseLayer": false, "name": "Nexrad", "url": "http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi", "subdomains": [], "displayInLayerSwitcher": false, "token": ""}, {"styles": "", "layer": "", "enableIdentify": false, "layer_info_link": null, "downloadableLink": "", "spatialReference": "EPSG:4326", "id": 3, "maplayer_id": 2, "shown": true, "layerParsingFunction": null, "rootField": "", "type": "WMS", "infoFormat": null, "opacity": 0.8, "dynamicParams": null, "attribution": "", "description": "", "format": "png24", "fieldsToShow": "", "zIndex": 1, "layerParams": {"dpi": 92, "f": "image"}, "transparent": true, "refreshrate": null, "isBaseLayer": false, "name": "National Map", "url": "http://raster.nationalmap.gov/ArcGIS/rest/services/TNM_Large_Scale_Imagery/MapServer/export", "subdomains": [], "displayInLayerSwitcher": false, "token": ""}], "projection": "EPSG:4326", "all_layers": "[{\\"layer\\": \\"\\", \\"enableIdentify\\": false, \\"layer_info_link\\": null, \\"downloadableLink\\": \\"\\", \\"spatialReference\\": \\"EPSG:4326\\", \\"id\\": 5, \\"dynamicParams\\": null, \\"layerParsingFunction\\": null, \\"rootField\\": \\"\\", \\"type\\": \\"GeoJSON\\", \\"infoFormat\\": null, \\"styles\\": \\"\\", \\"attribution\\": \\"\\", \\"description\\": \\"\\", \\"format\\": null, \\"fieldsToShow\\": \\"\\", \\"layerParams\\": {}, \\"transparent\\": true, \\"refreshrate\\": null, \\"name\\": \\"Chicago Zip Codes\\", \\"url\\": \\"https://raw.github.com/smartchicago/chicago-atlas/master/db/import/zipcodes.geojson\\", \\"subdomains\\": [], \\"token\\": \\"\\"}, {\\"layer\\": \\"\\", \\"enableIdentify\\": false, \\"layer_info_link\\": null, \\"downloadableLink\\": \\"\\", \\"spatialReference\\": \\"EPSG:4326\\", \\"id\\": 6, \\"dynamicParams\\": null, \\"layerParsingFunction\\": null, \\"rootField\\": \\"\\", \\"type\\": \\"GeoJSON\\", \\"infoFormat\\": null, \\"styles\\": \\"\\", \\"attribution\\": \\"\\", \\"description\\": \\"\\", \\"format\\": null, \\"fieldsToShow\\": \\"\\", \\"layerParams\\": {}, \\"transparent\\": true, \\"refreshrate\\": null, \\"name\\": \\"DC Bars\\", \\"url\\": \\"https://raw.github.com/benbalter/dc-wifi-social/master/bars.geojson\\", \\"subdomains\\": [], \\"token\\": \\"\\"}, {\\"layer\\": \\"AIRS_Precipitation_Day\\", \\"enableIdentify\\": false, \\"layer_info_link\\": null, \\"downloadableLink\\": \\"\\", \\"spatialReference\\": \\"EPSG:4326\\", \\"id\\": 7, \\"dynamicParams\\": [{\\"range\\": {\\"start\\": \\"2012-05-08\\", \\"type\\": \\"FixedRange\\"}, \\"type\\": \\"Date\\", \\"name\\": \\"Time\\"}], \\"layerParsingFunction\\": null, \\"rootField\\": \\"\\", \\"type\\": \\"WMTS\\", \\"infoFormat\\": null, \\"styles\\": \\"\\", \\"attribution\\": \\"\\", \\"description\\": \\"NASA Satellite\\", \\"format\\": \\"jpeg\\", \\"fieldsToShow\\": \\"\\", \\"layerParams\\": {\\"layer\\": \\"AIRS_Precipitation_Day\\", \\"TileMatrixSet\\": \\"GoogleMapsCompatible_Level6\\", \\"Time\\": \\"2014-11-04\\"}, \\"transparent\\": true, \\"refreshrate\\": null, \\"name\\": \\"NASA AIRS Precipitation Day\\", \\"url\\": \\"http://map1.vis.earthdata.nasa.gov/wmts-webmerc/AIRS_Precipitation_Day/default/{Time}/{TileMatrixSet}/{z}/{y}/{x}.png\\", \\"subdomains\\": [], \\"token\\": \\"\\"}, {\\"layer\\": \\"\\", \\"enableIdentify\\": false, \\"layer_info_link\\": null, \\"downloadableLink\\": \\"\\", \\"spatialReference\\": \\"EPSG:4326\\", \\"id\\": 3, \\"dynamicParams\\": null, \\"layerParsingFunction\\": null, \\"rootField\\": \\"\\", \\"type\\": \\"WMS\\", \\"infoFormat\\": null, \\"styles\\": \\"\\", \\"attribution\\": \\"\\", \\"description\\": \\"\\", \\"format\\": \\"png24\\", \\"fieldsToShow\\": \\"\\", \\"layerParams\\": {\\"dpi\\": 92, \\"f\\": \\"image\\"}, \\"transparent\\": true, \\"refreshrate\\": null, \\"name\\": \\"National Map\\", \\"url\\": \\"http://raster.nationalmap.gov/ArcGIS/rest/services/TNM_Large_Scale_Imagery/MapServer/export\\", \\"subdomains\\": [], \\"token\\": \\"\\"}, {\\"layer\\": \\"nexrad-n0r-900913\\", \\"enableIdentify\\": false, \\"layer_info_link\\": null, \\"downloadableLink\\": \\"\\", \\"spatialReference\\": \\"EPSG:4326\\", \\"id\\": 1, \\"dynamicParams\\": null, \\"layerParsingFunction\\": null, \\"rootField\\": \\"\\", \\"type\\": \\"WMS\\", \\"infoFormat\\": null, \\"styles\\": \\"\\", \\"attribution\\": \\"Weather data \\\\u00a9 2012 IEM Nexrad\\", \\"description\\": \\"\\", \\"format\\": \\"image/png\\", \\"fieldsToShow\\": \\"\\", \\"layerParams\\": {}, \\"transparent\\": true, \\"refreshrate\\": null, \\"name\\": \\"Nexrad\\", \\"url\\": \\"http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi\\", \\"subdomains\\": [], \\"token\\": \\"\\"}, {\\"layer\\": \\"\\", \\"enableIdentify\\": false, \\"layer_info_link\\": null, \\"downloadableLink\\": \\"\\", \\"spatialReference\\": \\"EPSG:4326\\", \\"id\\": 2, \\"dynamicParams\\": null, \\"layerParsingFunction\\": null, \\"rootField\\": \\"\\", \\"type\\": \\"ArcGIS Tiled Map Service\\", \\"infoFormat\\": null, \\"styles\\": \\"\\", \\"attribution\\": \\"\\", \\"description\\": \\"\\", \\"format\\": null, \\"fieldsToShow\\": \\"\\", \\"layerParams\\": {}, \\"transparent\\": true, \\"refreshrate\\": null, \\"name\\": \\"USA_Median_Household_Income\\", \\"url\\": \\"http://server.arcgisonline.com/ArcGIS/rest/services/Demographics/USA_Median_Household_Income/MapServer\\", \\"subdomains\\": [], \\"token\\": \\"\\"}]", "zoom": 15, "center_x": 0, "center_y": 0}')
    
    #Error from map.get_absolute_url() => NoReverseMatch: Reverse for 'map-update' with arguments '(1,)' and keyword arguments '{}' not found.
    #The url of 'map-update' requires job_id and map_id, but only map_id is provided in get_absolute_url() function.
    #def testGetAbsoluteUrl(self):
    #    """ -- Verify Absolute URL of Map"""
    #    map = Map.objects.get(id=1)
    #    url = map.get_absolute_url()
    #    self.assertEqual(url, "") 
        
        
class MapLayerTest(BaseTest):
    
    def testUnicode(self):
        """ -- Verify Layer stack order and name of MapLayer"""
        maplayer = MapLayer.objects.get(id=1)
        self.assertEqual(unicode(maplayer), "Layer 0: Nexrad")

#AttributeError: type object 'MapLayerUserRememberedParams' has no attribute 'objects'        
#class MapLayerUserRememberedParams(BaseTest):
    
    #def testMap(self):
        #""" -- Verify map of MapLayerUserRememberedParams"""
        #params = MapLayerUserRememberedParams.objects.get(id=1)
        #pk = parmas.map()
        #assertEqual(pk, None)
 
#AttributeError: type object 'EditableMapLayer' has no attribute 'objects'       
#class EditableMapLayer(BaseTest):
    
    #def testUnicode(self):
        #""" -- Verify name and type of EditableMapLayer"""
        #maplayer = EditableMapLayer.objects.get(id=1)
        #assertEqual(unicode(maplayer), None)
        
class FeatureTest(BaseTest):
    
    def testGeoJSON(self):
        """ -- Verify Feature using JSON format"""
        feature = Feature.objects.get(id=71)
        self.assertEqual(feature.geoJSON(), '{"type": "Feature", "properties": {"status": "In work", "name": "severity", "created_at": "2013-12-04T19:09:37UTC", "updated_at": "2013-12-04T19:09:37UTC", "analyst": "admin", "template": 1, "type": "text", "id": 71}, "geometry": {"type": "Polygon", "coordinates": [[[-74.0692663192749, 40.129016064673706], [-74.0692663192749, 40.13075512411209], [-74.06729221343994, 40.13075512411209], [-74.06729221343994, 40.129016064673706], [-74.0692663192749, 40.129016064673706]]]}, "style": {"stroke-width": 2, "opacity": 1, "stroke-color": "red", "fill-color": "red"}}')
        
    def testJsonItem(self):
        """ -- Verify JSON item"""
        feature = Feature.objects.get(id=71)
        self.assertEqual(feature.json_item(), {'status': 'In work', 'feature_type': 'Catastrophic Damage', 'linked_items': False, 'id': 71, 'county': 'Unknown', 'workcell_id': 6513, u'type': u'name', 'analyst': 'admin'})
        
        
    def testUnicode(self):
        """ -- Verify Feature name"""
        feature = Feature.objects.get(id=71)
        self.assertEqual(unicode(feature), "Feature created for Jersey Shore Damage Assessment")
        
    def testClean(self):
        """ -- Verify geometry type"""
        feature = Feature.objects.get(id=71)
        self.assertEqual(feature.clean(), None)
        
class FeatureTypeTest(BaseTest):
    
    def testToJson(self):
        """ -- Verify FeatureType using JSON format"""
        featuretype = FeatureType.objects.get(id=1)
        json = featuretype.to_json()
        self.assertEqual(json, '{"category": "", "style": {"color": "red", "opacity": 1, "weight": 2}, "name": "Catastrophic Damage", "id": 1, "order": 0, "type": "Polygon", "properties": [{"type": "text", "name": "severity"}], "icon": ""}')
        
    def testIconized(self):
        """ -- Verify FeatureType icon"""
        featuretype = FeatureType.objects.get(id=1)
        html = featuretype.iconized()
        self.assertEqual(html, "<span style='height:25px; border-width:2px; border-color:red; background-color:red; border-radius:4px; display:inline-block; opacity:1; width:25px;'> &nbsp; </span>")
        
    def testStyleJson(self):
        """ -- Verify FeatureType style JSON """
        featuretype = FeatureType.objects.get(id=1)
        style = featuretype .style_json()
        self.assertEqual(style, '{"color": "red", "opacity": 1, "weight": 2}')
        
    def testFeaturetypes(self):
        """ -- Verify all FeatureTypes"""
        featuretypes = FeatureType.objects.all()
        self.assertEqual(featuretypes.count(), 7)
        
    def testGetAbsoluteUrl(self):
        """ -- Verify FeatureType absolute url"""
        featuretype = FeatureType.objects.get(id=1)
        url = featuretype.get_absolute_url()
        self.assertEqual(url, "/maps/feature-types/update/1")
        
    def testUnicode(self):
        """ -- Verify name of FeatureType"""
        featuretype = FeatureType.objects.get(id=1)
        self.assertEqual(unicode(featuretype), "Catastrophic Damage")
        
        
        