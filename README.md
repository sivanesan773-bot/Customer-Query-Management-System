# Customer-Query-Management-System
This project is created for customer query management system


**Home Page :**
enter user name
enter user password
select role in the drop down (the user name & password should be with respect to Roles ) | (Client | Support)


**Client Page :**
Enter query Heading , description, maild id, mobile number, the created date and qid will be autiomatically generated and get update in the mysql database


**support Page :**
Fist gives option to view the open or closed query via drop down


**open query page :**
list down 10 open query details in assending order and give support people to enter the resolution and update the status as CLOSED, once clicking the update button the resolutionclosed date and status will get updated in the MYsql database WRT qid


**Closed Query Page :**
list down 10 open query details in desending order and give support people to viwe recently closed query and resolution


username and password fopr each role is embeded in separate file(cred.py)

