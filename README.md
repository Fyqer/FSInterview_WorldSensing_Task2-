# FSInterview_WorldSensing_Task3-
# Stack: 
Flask and python
# Files:
Configs.html - Retrieving all configurations for all sensor models.
SpecyficSensor - Getting configuration for a specific sensor model.
/templates - additionaly html templates from tasks 4
app.py - main logic with routes
handlers.py - handlers methods, saving to file.
style.css - additionaly from task 4
# Routes:
localhost:/ - main page with layout
localhost:/<sensor_model> - configuration for specific sensor
localhost:/Configs - all configurations 
localhost:/create/<model>/<output>/<handler> - creating config
localhost//Handleit/<string:model>/<string:handler>/<string:output> - handling

