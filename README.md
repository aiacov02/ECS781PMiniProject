# ECS781PMiniProject #

<h3> Rest API for the ECS781P-Cloud Computing mini-project <h4>

This Rest API was created under the framework of the ECS781P Cloud Computing module,
from the Queen Mary, University of London. <br/>
<br />
The API utilizes the MET police API and the Google Place API to fetch crime data.
<br/>
To use the API, username and password or token based authentication is required.

<h4> LICENCE </h4>

Please see License.txt file
<br/>

<h4> Running instructions <h4>

1. Download or clone the directory
2. Setup and run Cassandra database on localhost.
3. Replace the API_KEY in the server.py file with a working Google Places API key.
4. From the root directory run python server.py in the terminal 

<h4> Google Cloud Engine Installation Instructions </h4>
1. Download or clone reporistory<br/>
2. Replace the API_KEY in the server.py file with a working Google Places API key.<br/
3. Run Docker Build<br/>
4. Run Docker Push<br/>
5. Run kubectl create -f cassandra-peer-service-yml <br/>
6. Run kubectl create -f cassandra-service.yml<br/>
7. Run kubectl create -f cassandra-replication-controller.yml<br/>
8. Run kubectl apply -f ccminiprojectDeployment.yaml<br/>
9. Run kubectl apply -f ccminiprojectservice.yaml<br/>



<h4> REST API Requests </h4>
<br/>

Please note: this REST API uses a self signed certificate for SSL encryption. The curl command doesn't like self signed
certificates and will not allow any requests to be made. Therefore, in order be able to make a request run all the
below commands using <strong> sudo </strong> and the command parameter <strong> --cacert cacert.pem </strong> where
cacert.pem is the certificate file inside the root directory of the project.

<strong>Request</strong>

* Intro message<br/>
GET / <br/>
<code>  curl -i https://localhost:5000/ </code>
   
<strong>Response</strong>

```json
<code> HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 114
Server: Werkzeug/0.14.1 Python/2.7.16
Date: Sat, 23 Mar 2019 21:06:23 GMT

 {
  "data": "Welcome to the Cloud Computing Mini Project REST API. To start using the API please create a user"
}
</code>
```

<strong>Request</strong>

* Create user:<br/>
POST /api/users/createuser <br/>
<code>curl -H "Content-Type: application/json" -d '{"username":"your_username","password":"your_password","name":"your_name","email":"your_email"}' -X POST 'https://localhost:5000/api/users/createuser'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 201 CREATED <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


{
  "email": "your_email", 
  "name": "your_name", 
  "username": "your_username"
}</code>


<strong>Request</strong>

* Request authentication token:<br/>
GET / <br/>
<code>curl -i -u username:password 'https://localhost:5000/api/token'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 201 CREATED <br/>
Content-Type: application/json <br/>
Content-Length: 232 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


{
  "token": "AUTHENTICATION_TOKEN"
}</code>

<strong>Request</strong>

* Update user:<br/>
PUT /api/users/updateuser/username_to_update <br/>
<code>curl -i -u authentication_token:unused -H "Content-Type: application/json" -d '{"password":"your_password","name":"your_name","email":"your_email"}' -X PUT 'https://localhost:5000/api/users/updateuser/username_to_update'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 200 SUCCESS <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


'{
  "email": "your_email", 
  "name": "your_name", 
  "username": "your_username"
}'
</code>

<strong>Request</strong>

* Delete user:<br/>
DELETE /api/users/deleteuser/username_to_delete <br/>
<code>curl -i -u authentication_token:unused -X DELETE 'https://localhost:5000/api/users/deleteuser/username_to_delete'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 200 SUCCESS <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


'{
  "data": "user deleted"
}'</code>

<strong>Request</strong>

* Get crimes near a specific latitude, longitude and date:<br/>
GET /api/get_crimes <br/>
<code>curl -i -u authentication_token:unused 'https://localhost:5000/api/get_crimes?lat=LAT&lng=LNG&date=DATE'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 200 SUCCESS <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


'{
  "data": CRIME DATA
}'</code>

<strong>Request</strong>

* Get crimes near a specific place, giving its name:<br/>
GET /api/get_crimes_at_place <br/>
<code>curl -i -u authentication_token:unused 'https://localhost:5000/api/get_crimes_at_place?place=PLACE'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 200 SUCCESS <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


'{
  "data": CRIME DATA
}'</code>


<strong>Request</strong>

* Get outcome of a specific crime<br/>
GET /api/get_crime_outcome <br/>
<code>curl -i -u authentication_token:unused 'https://localhost:5000/api/get_crime_outcome?id=CRIME_ID'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 200 SUCCESS <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


'{
  "data": CRIME DATA
}'</code>

<strong>Request</strong>

* Get crime categories available at a specific date<br/>
GET /api/get_crime_categories <br/>
<code>curl -i -u authentication_token:unused 'https://localhost:5000/api/get_crime_categories?date=DATE'</code>
   
<strong>Response</strong>

<code>HTTP/1.0 200 SUCCESS <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>


'{
  "data": CRIME CATEGORIES
}'</code>
