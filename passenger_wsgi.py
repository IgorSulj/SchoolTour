import sys, os 
cwd = os.getcwd() 
sys.path.append(cwd) 
os.environ['DJANGO_SETTINGS_MODULE'] = "schooltour.settings"
from django.core.wsgi import get_wsgi_application 
application = get_wsgi_application()