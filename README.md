# ECS781PMiniProject

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

   * Create user<br/>
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
   GET / <br/>
   <code>  curl -H "Content-Type: application/json" -d '{"username":"your_username","password":"your_password","name":"your_name","email":"your_email"}' -X POST 'https://localhost:5000/api/users/createuser'
 </code>
   
<strong>Response</strong>

<code> HTTP/1.0 201 CREATED <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>

{
  "email": "your_email", 
  "name": "your_name", 
  "username": "your_username"
}

</code>

<strong>Request</strong>

   * Update user:<br/>
   GET / <br/>
   <code>  curl -H "Content-Type: application/json" -d '{"password":"your_password","name":"your_name","email":"your_email"}' -X PUT 'https://localhost:5000/api/users/updateuser/<user>'
 </code>
   
<strong>Response</strong>

<code> HTTP/1.0 200 SUCCESS <br/>
Content-Type: application/json <br/>
Content-Length: 85 <br/>
Server: Werkzeug/0.14.1 Python/2.7.16 <br/>
Date: Sat, 23 Mar 2019 21:25:50 GMT <br/>

{
  "email": "your_email", 
  "name": "your_name", 
  "username": "your_username"
}

</code>



