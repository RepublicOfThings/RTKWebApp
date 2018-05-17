
VERSION = "0.3.0"

USERNAME = "smeiling"
PASSWORD = "qAk6XJLedAeD"
HOST = "37.48.244.182"
PORT = "8000"
ALERT_DASHBOARD = "incident_posture_clone_v10"
HOMES_DASHBOARD = "smeiling_dashboard_mca_v10_splunk"
ALERT_APP = "alert_manager"
HOMES_APP = "rot_smart_homes_app"
# http://37.48.244.182/en-US/account/insecurelogin?username=smeiling&password=qAk6XJLedAeD&return_to=app/rot_smart_homes_app/smeiling_dashboard_mca_v10_splunk
URL_TEMPLATE = "http://{host}:{port}/en-US/account/insecurelogin?username={user}&password={pwd}&return_to=app/{app}/{dash}"

# Legacy
ENDPOINT = None
