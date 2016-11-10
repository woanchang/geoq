import sys
import json
from django.test import TestCase
from django.test import RequestFactory 
from geoq.maps.models import *
from geoq.maps.views import *
from geoq.maps.forms import *
from django.core.urlresolvers import reverse

class BaseTest(TestCase):
    TestCase.maxDiff = None
    
class CreateFeaturesTest(BaseTest):
    def testPost(self):
        """ -- Verify the Post method to create Feature"""
        data = {'aoi': 6513, 'geometry':{'type': "Point", 'coordinates': [40.126801, -74.066584]}}
        response = self.client.post(reverse('feature-create'), data)
        self.assertEqual(response.status_code, 302)
       
class EditFeaturesTest(BaseTest):
    def testPost(self):
        """ -- Verify the Post method to edit Feature"""
        data = {'aoi': 6513, 'geometry':{'type': "Polygon", 'coordinates': [[[-74.569266, 40.129016],
                [-74.569266, 40.130755], [-74.567292, 40.130755],[-74.567292, 40.129016],[-74.569266, 40.129016]]]},'properties': {'id': 71}}
        response = self.client.post(reverse('feature-edit'), data)
        self.assertEqual(response.status_code, 302)
    
    #To Do    
    def testUpdateUserMaplayerParam(self):
        """ -- Verify a function to update maplayer parameters"""
        data = {'maplyer': 1, 'param': "layer", 'newValue': "2"}
        response = self.client.post(reverse('update-user-maplayer-param'), data)
        self.assertEqual(response.status_code, 302)
    
    #To Do: No URL for feature-delete in urls.py    
    def testFeatureDelete(self):
        """ -- Verify a function to delete Feature"""
        pass
    
class MapListViewTest(BaseTest):
    def testGetContextData(self):
        """ -- Verify the Queryset for MapListView"""
        response = self.client.get(reverse('map-list'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['map_list'])      
        self.assertEqual(count, 2, "Expected 2 maps, found %s instead" % (count))
        self.assertEqual(response.context['admin'], False)
    
class MapDeleteTest(BaseTest):
    def testGetSuccessUrl(self):
        """ -- Verify MapDelete"""
        map = Map.objects.get(id=1)
        response = self.client.get(reverse('map-delete', kwargs={'pk': map.pk}))
        self.assertEqual(response.status_code, 302)
        
class FeatureTypeListViewTest(BaseTest):
    def testGetContextData(self):
        """ -- Verify the Queryset for FeatureTypeListView"""
        response = self.client.get(reverse('feature-type-list'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['featuretype_list'])     
        self.assertEqual(count, 7, "Expected 7 featuretypes, found %s instead" % (count))
        self.assertEqual(response.context['admin'], False)
        
class FeatureTypeDeleteTest(BaseTest):
    def testGetSuccessUrl(self):
        """ -- Verify the function to delete FeatureType"""
        featuretype = FeatureType.objects.get(id=1)
        response = self.client.get(reverse('feature-type-delete', kwargs={'pk': featuretype.pk}))
        self.assertEqual(response.status_code, 302)
        
class LayerListViewTest(BaseTest):
    def testGetContextData(self):
        """ -- Verify the Queryset for LayerListView"""
        response = self.client.get(reverse('layer-list'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['layer_list'])
        self.assertEqual(count, 6, "Expected 6 layers, found %s instead" % (count))
        
class LayerImport(BaseTest):
    def testGetContextData(self):
        """ -- Verify the context data for LayerImport"""
        response = self.client.get(reverse('job-list'))
        response = self.client.get(reverse('layer-import'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['geoevents_sources'])
        self.assertEqual(count, 0, "Expected 0 layers, found %s instead" % (count))

    def testPost(self):
        """ -- Verify the Post method to add new layers"""
        data = {'name': "perm_water_polygon", 'type': "WFS", 'url': "http://geoserver.ics.perm.ru/geoserver/ows"}
        response = self.client.post(reverse('layer-import'), data)
        self.assertEqual(response.status_code, 302)
        
class LayerDeleteTest(BaseTest):
    def testGetSuccessUrl(self):
        """ -- Verify LayerDelete"""
        layer = Layer.objects.get(id=1)
        response = self.client.get(reverse('layer-delete', kwargs={'pk': layer.pk}))
        self.assertEqual(response.status_code, 302)
    
class KMZLayerImport(BaseTest):
    def testGetContextData(self):
        """ -- Verify the context data for KMZLayerImport"""
        response = self.client.get(reverse('create-kml-layer'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['layer_list'])
        self.assertEqual(count, 6, "Expected 6 layers, found %s instead" % (count))
        
    #TO DO: Need a kmz or kml file to test.
    #def testPost(self):
        #""" -- Verify the Post method to upload KML or KMZ file and create a new layer"""
        #kmzfile = open('kmzfile.txt', 'r')
        #response = self.client.post(reverse('create-kml-layer'), kmzfile)
        #self.assertEqual(response.status_code, 302)
        
    
        
    
    
    

        
        