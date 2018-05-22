from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_deny
from .app_settings import *
# Create your views here.
# incident_posture_clone_v10

@xframe_options_deny
def home(request):
    return HttpResponse(render(request, 'pages/home/index.html', {"title": "Home", "endpoint": ENDPOINT, "version": VERSION,
                                                                  "year": datetime.datetime.now().year}))


@xframe_options_deny
def contact(request):
    return HttpResponse(render(request, 'pages/contact/index.html', {"title": "Contact", "endpoint": ENDPOINT,"version": VERSION,
                                                                        "year": datetime.datetime.now().year}))


@xframe_options_exempt
def alerts(request):
    target = URL_TEMPLATE.format(user=USERNAME, pwd=PASSWORD, app=ALERT_APP, dash=ALERT_DASHBOARD, host=HOST, port=PORT)
    return HttpResponse(render(request,
                               'pages/dashboard/index.html',
                               {"title": "Incident Posture (Live Demo)",
                                "target": target,
                                "version": VERSION,
                                "year": datetime.datetime.now().year}))

@xframe_options_exempt
def dashboard(request):
    target = URL_TEMPLATE.format(user=USERNAME, pwd=PASSWORD, app=HOMES_APP, dash=HOMES_DASHBOARD, host=HOST, port=PORT)
    return HttpResponse(render(request,
                               'pages/dashboard/index.html',
                               {"title": "Connected Homes (Live Demo)",
                                "target": target,
                                "version": VERSION,
                                "year": datetime.datetime.now().year}))


@xframe_options_exempt
def available(request):
    return HttpResponse(render(request,
                               'pages/dashboards/index.html',
                               {"title": "Available Dashboards",
                                "version": VERSION,
                                "year": datetime.datetime.now().year}))

@xframe_options_deny
def holding(request):
    return HttpResponse(render(request, 'common/holding.html', {"title": "Holding", "version": VERSION}))


@xframe_options_deny
def testbed(request):
    import requests
    s = requests.Session()
    r = s.post("http://37.48.244.187:8000/login", data={"username": "testuser1", "password": "mCAuSERACCESS"})
    return HttpResponse(render(request, 'common/holding.html', {"title": "Holding", "version": VERSION, "data": r.content}))


# Deprecated


@xframe_options_exempt
def configure_filter(request):
    return HttpResponse(render(request, 'pages/launch/filter/index.html', {"title": "Filter", "device": "Filter", "endpoint": ENDPOINT,
                                                                      "id": None,
                                                                      "year": datetime.datetime.now().year}))


@xframe_options_exempt
def configure_target_filter(request, instance=None):
    return HttpResponse(render(request, 'pages/launch/filter/index.html', {"title": "Filter", "device": "Filter", "endpoint": ENDPOINT,
                                                                      "id": instance,
                                                                      "year": datetime.datetime.now().year}))


@xframe_options_exempt
def configure_target_sensor(request, instance=None):
    return HttpResponse(render(request, 'pages/launch/sensor/index.html', {"title": "Sensor", "device": "Sensor", "endpoint": ENDPOINT,
                                                                      "id": instance,
                                                                      "year": datetime.datetime.now().year}))


@xframe_options_exempt
def configure_sensor(request):
    return HttpResponse(render(request, 'pages/launch/sensor/index.html', {"title": "Sensor", "device": "Sensor", "endpoint": ENDPOINT,
                                                                      "id": None,
                                                                      "year": datetime.datetime.now().year}))


@xframe_options_exempt
def manage_instances(request):
    return HttpResponse(render(request, 'pages/manage/instances/index.html', {"title": "Manage", "endpoint": ENDPOINT,
                                                                      "year": datetime.datetime.now().year}))


@xframe_options_exempt
def admin_controls(request):
    return HttpResponse(render(request, 'pages/manage/admin/index.html', {"title": "Admin", "endpoint": ENDPOINT,
                                                                      "year": datetime.datetime.now().year}))


@xframe_options_exempt
def monitor_overview(request):
    return HttpResponse(render(request, 'pages/tools/overview/index.html', {"title": "Overview", "endpoint": ENDPOINT,
                                                                      "year": datetime.datetime.now().year}))


@xframe_options_exempt
def monitor_analysis(request):
    return HttpResponse(render(request, 'pages/tools/analysis/index.html', {"title": "Analysis", "endpoint": ENDPOINT,
                                                                              "year": datetime.datetime.now().year}))


@xframe_options_exempt
def monitor_visualise(request):
    return HttpResponse(render(request, 'pages/tools/visualise/index.html', {"title": "Visualise", "endpoint": ENDPOINT,
                                                                                "year": datetime.datetime.now().year}))


@xframe_options_exempt
def monitor_visualise(request):
    return HttpResponse(render(request, 'pages/tools/visualise/index.html', {"title": "Visualise", "endpoint": ENDPOINT,
                                                                                "year": datetime.datetime.now().year}))


@xframe_options_exempt
def handler(request):
    return HttpResponse(render(request, 'common/error.html', {"title": "Error", "code": "Unknown", "endpoint": ENDPOINT,
                                                                                "year": datetime.datetime.now().year}))


@xframe_options_exempt
def handler400(request):
    return HttpResponse(render(request, 'common/error.html', {"title": "Error", "code": "400", "endpoint": ENDPOINT,
                                                                                "year": datetime.datetime.now().year}))


@xframe_options_exempt
def handler404(request):
    return HttpResponse(render(request, 'common/error.html', {"title": "Error", "code": "404", "endpoint": ENDPOINT,
                                                                                "year": datetime.datetime.now().year}))


@xframe_options_exempt
def handler500(request):
    return HttpResponse(render(request, 'common/error.html', {"title": "Error", "code": "500", "endpoint": ENDPOINT,
                                                                                "year": datetime.datetime.now().year}))


@xframe_options_exempt
def handler403(request):
    return HttpResponse(render(request, 'common/error.html', {"title": "Error", "code": "403", "endpoint": ENDPOINT,
                                                                                "year": datetime.datetime.now().year}))
