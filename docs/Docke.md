The practical workflow would be:

Train your model in your notebook.
Save the trained model as a .joblib file.
Create app.py to:
Receive MOF features.
Load the model.
Make a CO₂-uptake prediction.
Save the inputs and prediction in PostgreSQL.
Return the prediction to the user.
Create a Dockerfile for the Python application.
Define app and database services in docker-compose.yml.
Start both containers with docker-compose up --build.
Send a prediction request from your computer.
The app makes the prediction and writes a database record.

A stored prediction might contain:

Database column	Example
void_fraction	0.67
pld	6.2
lcd	8.4
surface_area_m2g	1450
predicted_co2_uptake	3.71
created_at