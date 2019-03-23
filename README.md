# ECS781PMiniProject #

<h3> Rest API for the ECS781P-Cloud Computing mini-project <h4>

This Rest API was created under the framework of the ECS781P Cloud Computing module,
from the Queen Mary, University of London. <br/>
<br />
The API utilizes the MET police API and the Google Place API to fetch crime data.
<br/>
To use the API, authentication is required.

<h4> LICENCE </h4>

Please see License.txt file
<br/>

<h4> REST API Requests </h4>
<br/>

<strong>Request</strong>

* Intro message<br/>
GET / <br/>
<code>  curl -i http://localhost:5000/ </code>
   
<strong>Response</strong>

<code> HTTP/1.0 200 OK <br/>
Content-Type: application/json<br/>
Content-Length: 114 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:06:23 GMT <br/>

 {
  "data": "Welcome to the Cloud Computing Mini Project REST API. To start using the API please create a user"
}
</code>

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
