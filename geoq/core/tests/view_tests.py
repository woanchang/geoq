import sys
import json
from django.test import TestCase
from django.test import RequestFactory 
from geoq.core.models import *
from geoq.core.views import *
from geoq.core.forms import *

class BaseTest(TestCase):
    #fixtures = ['geoq_core_test_data.json']
    
    def setUp(self):
        comment_user = User.objects.get(id=4)
        comment_aoi = AOI.objects.get(id=6508)
        Comment.objects.create(user=comment_user, aoi=comment_aoi, text="Test Log")
        Organization.objects.create(name="MITRE")

class DashboardTest(BaseTest):
    def testDashboard(self):
        """ -- Verify the context data for Home page"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'core/dashboard.html')
        count = response.context['count_users']
        self.assertEqual(count, 7, "Expected 7 users, found %s instead" % (count))
        count = response.context['count_jobs']
        self.assertEqual(count, 3, "Expected 3 jobs, found %s instead" % (count))
        count = response.context['count_workcells_total']
        self.assertEqual(count, 522, "Expected 522 workcells, found %s instead" % (count))
        count = response.context['count_training']
        self.assertEqual(count, 0, "Expected 0 trainings, found %s instead" % (count))
        projects = response.context['projects_private']
        count = len(projects)
        self.assertEqual(count, 0, "Expected 0 private project, found %s instead" % (count))
        count = response.context['count_projects_active']
        self.assertEqual(count, 1, "Expected 1 active project, found %s instead" % (count))
        count = response.context['count_projects_archived']
        self.assertEqual(count, 0, "Expected 0 archived project, found %s instead" % (count))
        count = response.context['count_projects_exercise']
        self.assertEqual(count, 0, "Expected 0 archived project, found %s instead" % (count))
        orgs = response.context['orgs']
        count = len(orgs)
        self.assertEqual(count, 0, "Expected 0 organization to be shown on front, found %s instead" % (count))
 
 #To Do       
class BatchCreateAOISTest(BaseTest):
        
    def testPost(self):
        """ -- Verify the post method for BatchCreateAOIS page"""
        job = Job.objects.get(name='Jersey Shore Damage Assessment')
        aois = [{
            "properties": {
                "status": "Unassigned",  
                "priority": 5
            }, 
            "geometry": "MULTIPOLYGON (((-77.6885826076872661 37.7096262076038045, -77.6932838803504353 37.7095188445385219, -77.6985388482057857 37.7093986023980108, -77.6999152954815884 37.7093670457647931, -77.7002422809125051 37.7183703532559775, -77.6988656357107459 37.7184019207936245, -77.6936100333682731 37.7185222017400719, -77.6889082247975296 37.7186295987342177, -77.6885826076872661 37.7096262076038045)))", 
        }]
        
        response = self.client.post(reverse('job-create-aois', kwargs={'job_pk':job.pk}), {'aois':aois})
        self.assertEqual(response.status_code, 302)
        
class TabbedProjectListViewTest(BaseTest):
        
    def testTabbedProjectListView(self):
        """ -- Verify the context data for Tabbed Project List page"""
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['private'])
        self.assertEqual(count, 0, "Expected 0 private project, found %s instead" % (count))
        count = len(response.context['archived'])
        self.assertEqual(count, 0, "Expected 0 archived project, found %s instead" % (count))
        count = len(response.context['exercise'])
        self.assertEqual(count, 0, "Expected 0 exercise project, found %s instead" % (count))
        count = len(response.context['active'])
        self.assertEqual(count, 1, "Expected 1 active project, found %s instead" % (count))
        self.assertEqual(response.context['active_pane'], 'active')
        
class TabbedJobListViewTest(BaseTest):
    
    def testTabbedJobListView(self):
        """ -- Verify the context data for TabbedJobListView"""
        response = self.client.get(reverse('job-list'))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['private'])
        self.assertEqual(count, 0, "Expected 0 private job, found %s instead" % (count))
        count = len(response.context['archived'])
        self.assertEqual(count, 0, "Expected 0 archived job, found %s instead" % (count))
        count = len(response.context['exercise'])
        self.assertEqual(count, 0, "Expected 0 exercise job, found %s instead" % (count))
        count = len(response.context['active'])
        self.assertEqual(count, 3, "Expected 3 active job, found %s instead" % (count))
        self.assertEqual(response.context['active_pane'], "active")
        
class DetailedListViewTest(BaseTest):
    
    def testDetailedListView(self):
        """ -- Verify the Queryset for DetailedListView"""
        project = Project.objects.get(name="Hurricane Sandy")
        response = self.client.get(reverse('project-detail', kwargs={'pk': project.pk }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/project_detail.html')
        count = len(response.context[8]['job_list'])      
        self.assertEqual(count, 3, "Expected 3 jobs, found %s instead" % (count))
    
#ToDo
class CreateFeaturesViewTest(BaseTest):
    
    def testGetContextData(self):
        """ -- Verify the context data of CreateFeatures View"""
        response = self.client.get(reverse('aoi-work', kwargs={'pk': 6465}))
        self.assertEqual(response.status_code, 302)
      
class JobDetailedListViewTest(BaseTest):
    
    def testJobDetailedListView(self):
        """ -- Verify Get method"""
        job = Job.objects.get(name='Exploit CAP Imagery')
        response = self.client.get(reverse('job-detail', kwargs={'pk': job.pk, 'status': 'active'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/job_detail.html')
        count = len(response.context['statuses'])
        self.assertEqual(count, 6, "Expected 6 statuses, found %s instead" % (count))
        self.assertEqual(response.context['active_status'], "active")
        self.assertEqual(response.context['workcell_count'], 47)
        self.assertEqual(response.context['metrics'], False)
        self.assertEqual(response.context['metrics_url'], "/geoq/jobs/metrics/1")
        self.assertEqual(response.context['completed'], 0.0)
        
class JobDeleteTest(BaseTest):
    
    def testJobDeletePage(self):
        """ -- Verify JobDelete"""
        job = Job.objects.get(name='Exploit CAP Imagery')
        response = self.client.get(reverse('job-delete', kwargs={'pk': job.pk}))
        self.assertEqual(response.status_code, 302)
        
class AOIDeleteTest(BaseTest):
    
    def testAOIDeletePage(self):
        """ Verify AOIDelete"""
        aois = AOI.objects.all().filter(name__iexact='Exploit CAP Imagery')
        response = self.client.get(reverse('aoi-delete', kwargs={'pk': aois[0].pk}))
        self.assertEqual(response.status_code, 200)
        
class AOIDetailedListViewTest(BaseTest):
        
    def testGetQueryset(self):
        """ -- Verify queryset"""
        aois = AOI.objects.all()
        view = AOIDetailedListView()
        view.kwargs = dict(status="active")
        self.assertQuerysetEqual(view.get_queryset(), map(repr, aois))
        
    def testGet(self):
        """ -- Verify get method"""
        response = self.client.get(reverse('aoi-list', kwargs={'status': 'active'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/aoi_list.html")
        
    def testGetContextData(self):
        """ -- Verify the context data"""
        response = self.client.get(reverse('aoi-list', kwargs={'status': 'active'}))
        self.assertEqual(response.status_code, 200)
        count = len(response.context['statuses'])
        self.assertEqual(count, 6, "Expected 6 statuses, found %s instead" % (count))
        self.assertEqual(response.context['active_status'], "active")
        
class CreateProjectViewTest(BaseTest):
    
    def testFormValid(self):
        """ -- Verify form_valid method"""
        request = RequestFactory().get(reverse('project-create'))
        view = CreateProjectView(template_name="core/generic_form.html")
        request.user = 1
        view.request =request
        form_data = {'name': 'Test Project', 'description':'Test', 'project_type': 'Flood'}
        form = ProjectForm(data=form_data)
        response = view.form_valid(form)
        self.assertEqual(response.status_code, 302)  #redirection found
 
 #To Do       
class CreateJobViewTest(BaseTest):
    
    def testCreateJobView(self):
        """ -- Verify CreateJob View"""
        response = self.client.get(reverse('job-create'))
        self.assertEqual(response.status_code, 302)
#To Do        
class UpdateJobViewTest(BaseTest):
    
    def testUpdateJobView(self):
        """ -- Verify UpdateJob View"""
        response = self.client.get(reverse('job-update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)  #redirection found
        
class MapEditViewTest(BaseTest):
    
    def testMapEditView(self):     
        """ -- Verify MapEdit View"""
        response = self.client.get(reverse('aoi-mapedit', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)  #redirection found
    
class ChangeAOIStatusTest(BaseTest):
    
    def testGet(self):     
        """ -- Verify Get method of ChangeAOIStatus View"""
        response = self.client.get(reverse('aoi-update-status', kwargs={'pk': 1, 'status': "Completed"}))
        self.assertEqual(response.status_code, 302)  #redirection found
        
    def testPost(self):     
        """ -- Verify Post method of ChangeAOIStatus View"""
        aoi = AOI.objects.get(id=6515)
        feature_ids = [81, 82, 83]
        response = self.client.post(reverse('aoi-update-status', kwargs={'pk': 6515, 'status': "Awaiting review"}), {'feature_ids': feature_ids})
        self.assertEqual(response.status_code, 302)  #redirection found
        
class PrioritizeWorkcellsTest(BaseTest):
        
    def testPost(self):
        """ -- Verify Post method of PrioritizeWorkcells View"""
        response = self.client.post(reverse('job-prioritize-workcells', kwargs={'job_pk': 1}), {'id': [6465, 6466], 'priority': [1,2]})
        self.assertEqual(response.status_code, 302)
        
class AssignWorkcellsViewTest(BaseTest):
    
    def testGet(self):
        """ -- Verify Get method of AssignWorkcells View"""
        response = self.client.get(reverse('job-assign-workcells', kwargs={'job_pk': 1}))
        self.assertEqual(response.status_code, 302)
        
    def testPost(self):
        """ -- Verify Post method of AssignWorkcells View"""
        response = self.client.post(reverse('job-assign-workcells', kwargs={'job_pk': 1}), {'workcells': [6465, 6466], 'user_type': "user", 'user_data': 3})
        self.assertEqual(response.status_code, 302)
        
class AOIDeleteTest(BaseTest):
    
    def testAOIDelete(self):
        """ -- Verify AOIDelete"""
        response = self.client.get(reverse('aoi-deleter', kwargs={'pk': 6465}))
        self.assertEqual(response.status_code, 302)
      
class LogJSONTest(BaseTest):
    
    def testLogJSON(self):
        """ -- Verify LogJSON"""
        response = self.client.get(reverse('workcell_log', kwargs={'pk': 6465}))
        self.assertEqual(response.status_code, 200)
        
class LayersJSONTest(BaseTest):
    
    def testLayersJSON(self):
        """ -- Verify LayersJSON"""
        response = self.client.get(reverse('json-layers'))
        self.assertEqual(response.status_code, 200)
    
class CellJSONTest(BaseTest):
    
    def testCellJSON(self):
        """ -- Verify CellJSON"""
        response = self.client.get(reverse('workcell_log', kwargs={'pk': 6465}))
        self.assertEqual(response.status_code, 200)
        
class JobGeoJSONTest(BaseTest):
    
    def testJobGeoJSON(self):
        """ -- Verify JobGeoJSON"""
        response = self.client.get(reverse('json-job', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        
class JobStyledGeoJSONTest(BaseTest):
    
    def testJobStyledGeoJSON(self):
        """ -- Verify JobStyledGeoJSON"""
        response = self.client.get(reverse('geojson-job-features', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        
class JobFeaturesJSONTest(BaseTest):
    
    def testJobFeaturesJSON(self):
        """ -- Verify JobFeaturesJSON"""
        response = self.client.get(reverse('json-job-features', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        
class GridGeoJSONTest(BaseTest):
    
    def testGridGeoJSON(self):
        """ -- Verify GridGeoJSON"""
        response = self.client.get(reverse('json-job-grid', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        
class TeamListViewTest(BaseTest):
    
    def testTeamListView(self):
        """ -- Verify TeamList View"""
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/team_list.html")

class CreateTeamViewTest(BaseTest):
    
    def testCreateTeamView(self):
        """ -- Verify CreateTeam View"""
        response = self.client.get(reverse('team-create'))
        self.assertEqual(response.status_code, 302)
        
class UpdateTeamViewTest(BaseTest):
    
    def testUpdateTeamView(self):
        """ -- Verify Post method of UpdateTeam View"""
        response = self.client.get(reverse('team-update', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        
class DeleteTeamViewTest(BaseTest):
    
    def testDeleteTeamView(self):
        """ -- Verify DeleteTeam View"""
        response = self.client.get(reverse('team-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)

                
        


    

        
    
        
    

    

    

        


