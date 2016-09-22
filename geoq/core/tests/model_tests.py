import sys
import datetime
import json
from django.test import TestCase
from geoq.core.models import *

class BaseTest(TestCase):
    fixtures = ['initial_data.json']
    
    def setUp(self):
        comment_user = User.objects.get(id=4)
        comment_aoi = AOI.objects.get(id=6508)
        Comment.objects.create(user=comment_user, aoi=comment_aoi, text="Test Log")
        Organization.objects.create(name="MITRE")
    

class ProjectTest(BaseTest):
        
    def testJobs(self):
        """ -- Verify jobs function of project"""
        project = Project.objects.get(name="Hurricane Sandy")
        jobs = project.jobs
        self.assertEqual(jobs.count(), 4)
        
    def testJobCount(self):
        """  -- Verify job count of a project"""
        project = Project.objects.get(name="Hurricane Sandy")
        count = project.job_count
        self.assertEqual(count, 4)
        
    def testUserCount(self):
        """  -- Verify user count of a project"""
        project = Project.objects.get(name="Hurricane Sandy")
        count = project.user_count
        self.assertEqual(count, 4)
        
    def testAois(self):
        """  -- Verify aois function of project"""
        project = Project.objects.get(name="Hurricane Sandy")
        aois = project.aois
        self.assertEqual(aois.count(), 554)
        
    def testAoiCount(self):
        """  -- Verify AOI count of a project"""
        project = Project.objects.get(name="Hurricane Sandy")
        count = project.aoi_count
        self.assertEqual(count, 554)
        
    #To Do
    def testAoisEnvelope(self):
        """  -- Verify a MultiPolygon for an envelope is returned."""
        project = Project.objects.get(name="Hurricane Sandy")
        envelope = project.aois_envelope
        self.assertIsInstance(envelope, MultiPolygon)
    
    #To Do    
    def testAoisEnvelopeByJob(self):
        """  -- Verify job envelops returned."""
        project = Project.objects.get(name="Hurricane Sandy")
        envelopes= project.aois_envelope_by_job    
        self.assertTrue(envelopes)
        
    def testGetAbsoluteUrl(self):
        """  -- Verify absolute url of project-detail page"""
        project = Project.objects.get(name="Hurricane Sandy")
        url = project.get_absolute_url()
        addr = "/geoq/projects/" + str(project.id)
        self.assertEqual(url, addr)
        
    def testGetUpdateUrl(self):
        """  -- Verify url of project-update page"""
        project = Project.objects.get(name="Hurricane Sandy")
        url = project.get_update_url()
        addr = "/geoq/projects/update/" + str(project.id)
        self.assertEqual(url, addr)
        
class JobTest(BaseTest):
    
    def testGetAbsoluteUrl(self):
        """  -- Verify absolute url of job-detail page"""
        job = Job.objects.get(name="Exploit CAP Imagery")
        url = job.get_absolute_url()
        addr = "/geoq/jobs/" + str(job.id) + "/"
        self.assertEqual(url, addr)
        
    def testGetUpdateUrl(self):
        """  -- Verify url of job-update page"""
        job = Job.objects.get(name="Exploit CAP Imagery")
        url = job.get_update_url()
        addr = "/geoq/jobs/update/" + str(job.id)
        self.assertEqual(url, addr)
        
    def testAoisGeometry(self):
        """  -- Verify AOI GEOMETYCOLLECTION"""
        job = Job.objects.get(name="Exploit CAP Imagery")
        aois = job.aois_geometry()
        self.assertEqual(len(aois), 43)
     
     #To Do   
    def testAoisEnvelope(self):
        """  -- Verify the envelope of related AOIs geometry."""
        job = Job.objects.get(name="Exploit CAP Imagery")
        envelope = job.aois_envelope()
        self.assertIsInstance(envelope, Polygon)
        #self.assertEqual(envelope, "POLYGON ((-77.7012239705196919 37.7008807834275004, -77.6315984307169344 37.7008807834275004, -77.6315984307169344 37.7739319203961941, -77.7012239705196919 37.7739319203961941, -77.7012239705196919 37.7008807834275004))")
        
    def testAoiCount(self):
        """  -- Verify AOI count of a job"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        count = job.aoi_count()
        self.assertEqual(count, 473)
        
    def testAoiCountsHtml(self):
        """  -- Verify AOI status count of a job"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        html = job.aoi_counts_html
        self.assertTrue("Completed: <b>17</b>, Unassigned: <b>456</b>" in html)
        
    def testUserCount(self):
        """  -- Verify user count of a job"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        count = job.user_count
        self.assertEqual(count, 4)
        
    def testBaseLayer(self):
        """  -- Verify base layer"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        layer = job.base_layer
        self.assertEqual(layer[0], "National Map")
        
    def testFeaturesTableHtml(self):
        """  -- Verify the content of Feature Count Table."""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        html = job.features_table_html()
        self.assertTrue("<tr><td><b>In work</b></td><td>23</td><td>4</td><td>4</td><td>7</td></tr>" in html)
        
    def testComplete(self):
        """  -- Verify the completed AOIs of a Job"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        aois = job.complete()
        self.assertEqual(aois.count(), 17)
        
    def testInWork(self):
        """  -- Verify the AOIs currently being worked on or in review"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        aois = job.in_work()
        self.assertEqual(aois.count(), 0)
        
    def testInWorkCount(self):
        """  -- Verify the count of the AOIs currently being worked on or in review"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        count = job.in_work_count()
        self.assertEqual(count, 0)
        
    def testCompleteCount(self):
        """  -- Verify the count of the completed AOIs """
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        count = job.complete_count()
        self.assertEqual(count, 17)
        
    def testCompletePercentCount(self):
        """  -- Verify the percentage of the completed AOIs """
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        percent = job.complete_percent()
        self.assertEqual(percent, 3.59)
        
    def testTotalCount(self):
        """ -- Verify the count of the total AOIs """
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        count = job.total_count()
        self.assertEqual(count, 473)
        
    def testGeoJSON(self):
        """ -- Verify geoJSON of the feature collection"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        geo_str = json.loads(job.geoJSON())
        self.assertEqual(len(geo_str["features"]), 473)
        
    def testGridGeoJSON(self):
        """ -- Verify geoJSON of grid for export"""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        grid = json.loads(job.grid_geoJSON())
        self.assertEqual(len(grid["features"]), 473)
        
    def testBaseLayerObject(self):
        """ -- Verify base layer object created to oeverride leaflet base OSM map."""
        job = Job.objects.get(name="Jersey Shore Damage Assessment")
        base_layer = job.base_layer_object()
        self.assertTrue("National Map" in base_layer["layers"][0])
        
        
class AOITest(BaseTest):
    
    def testUnicode(self):
        """ -- Verify AOI name and id returnd by __unicode__ function."""
        aoi = AOI.objects.get(id=6508)
        self.assertEqual(unicode(aoi), "Jersey Shore Damage Assessment - AOI 6508")
        
    def testLog(self):
        """ -- Verify AOI log comments."""
        aoi = AOI.objects.get(id=6508)
        self.assertEqual(len(aoi.log), 1)
        
    def testAssigneeName(self):
        """ -- Verify AOI assignee Name."""
        aoi = AOI.objects.get(id=6508)
        self.assertEqual(aoi.assignee_name, "Unknown")
        
    def testGetAbsoluteUrl(self):
        """ -- Verify AOI absolute url."""
        aoi = AOI.objects.get(id=6508)
        url = aoi.get_absolute_url()
        self.assertEqual(url, "/geoq/workcells/work/6508")
        
    def testGeoJSON(self):
        """ -- Verify the geoJSON of the AOI feature."""
        aoi = AOI.objects.get(id=6508)
        geo = json.loads(aoi.geoJSON())
        self.assertEqual(geo["properties"]["analyst"], "Suzy-supervisor")
        
    def testLogJSON(self):
        """ -- Verify AOI log object"""
        aoi = AOI.objects.get(id=6508)
        log = aoi.logJSON()
        self.assertEqual(log[0]["text"],"Test Log")
        
    def testPropertiesJson(self):
        """ -- Verify AOI properties"""
        aoi = AOI.objects.get(id=6508)
        properties = json.loads(aoi.properties_json())
        self.assertEqual(properties, {"priority": 5, "status": "Completed", "analyst": "Suzy-supervisor"})
        
    def testMapDetail(self):
        """ -- Verify map coordinates for MapEdit"""
        aoi = AOI.objects.get(id=6508)
        center = aoi.map_detail()
        self.assertEqual(center,"15/40.084035/-74.067512")
        
    def testGridGeoJSON(self):
        """ -- Verify the geoJSON of workcells for export."""
        aoi = AOI.objects.get(id=6508)
        geo = json.loads(aoi.grid_geoJSON())
        data = {'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[-74.06158572845553, 40.08849152466185], [-74.06170938959819, 40.07948306171372], [-74.06456441055161, 40.079506184260254], [-74.07000231929048, 40.07954997062946], [-74.07343658383317, 40.07957746226597], [-74.07331446806377, 40.08858595514634], [-74.06987972398599, 40.088558454566666], [-74.06444109865662, 40.08851465431222], [-74.06158572845553, 40.08849152466185]]]]}, 'type': 'Feature', 'properties': {'status': 'Completed', 'priority': 5, 'id': 6508}}
        self.assertEqual(geo, data)
        
    def testUserCanComplete(self):
        """ -- Verify whether the user can update the AOI as complete."""
        aoi = AOI.objects.get(id=6508)
        output = aoi.user_can_complete(aoi.analyst)
        self.assertTrue(output)
 #To Do   
class CommentTest(BaseTest):
    def testUnicode(self):
        """ -- Verify Comment user and AOI id returnd by __unicode__ function."""
        comment_aoi = AOI.objects.get(id=6508)
        comment = Comment.objects.get(aoi = comment_aoi)
        self.assertEqual(unicode(comment), "Suzy-supervisor Comment on 6508")
        
    def testToDict(self):
        """ -- VerifyComment ditionary."""
        comment_aoi = AOI.objects.get(id=6508)
        comment = Comment.objects.get(aoi = comment_aoi)
        dict = comment.to_dict()
        self.assertEqual(dict["text"], "Test Log")
        
class OrganizationTest(BaseTest):
    def testUnicode(self):
        """ -- Verify Comment user and AOI id returnd by __unicode__ function."""
        organization = Organization.objects.all()
        self.assertEqual(unicode(organization[0]), "MITRE")
    


    
        
    
    
        
        
        
    

    
    
        
        
        
        
      
 
        
        
        
        
        
        
        
    
        
        
        
        
        
    
        
        