# Django REST API Setup

This repository contains a Django project with a RESTful API using Django REST Framework.

## Prerequisites

- Python (version 3.x recommended)
- Django
- Django REST Framework

# Setup Instructions

## Create a Virtual Environment:
- python -m venv env

## Install Dependencies:
- pip install django
- pip install djangorestframework

## Set up a new project with a single application
- django-admin startproject Vendor                 
- cd Vendor
- django-admin startapp app              

## Database migration                    
- py manage.py makemigrations      
- py manage.py migrate

## Superuser creation and Token generation
- py manage.py createsuperuser

## Running the server
- py manage.py runserver

## Access Django Admin:
Open the Django admin at http://127.0.0.1:8000/admin/ and log in using the superuser credentials. this is to access the UI of database as a admin user.

## how to run a api endpoint:
- first we need to make sure that we migrated the models to database
- then we need to start the server using "py manage.py runserver" command.
- then we need to open another cmd prompt and open virtual environment and open the project folder and provide httpie commands.


# Testing or Using the API endpoints.
- we can test API endpoints using httpie commands. 

## Create a user:
### using httpie:
- http POST http://127.0.0.1:8000/api/register/ username="name" password="password"
### About this API endpoint:
- here this endpoint is used to create a user. Get response of Authorization Token key.

## Login User 
- http POST http://127.0.0.1:8000/api/login/ username="name" password="password"
### About this API endpoint:
- here this endpoint is used to login and Get response of Authorization Token key.

# Without Authorization Token key cann't access any API's


## Create a vendor:
### using httpie:
- http POST http://127.0.0.1:8000/api/vendor/ vendor_code=01 name="Vendor 1" contact_details="Contact 1" address="Address 1" "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to create a vendor by providing the vendor details.

## List all Vendors details:
### using httpie:
- http http://127.0.0.1:8000/api/vendor/ "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to get the details of all vendors.

## Retrieve a specific vendor's details:
### using httpie:
- http http://127.0.0.1:8000/api/vendor/{vendor_id}/ "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to get the details of vendor with vendor_id which was mentioned in the command. 

## Update a vendor's details:
### using httpie:
#### PUT method:
- http PUT http://127.0.0.1:8000/api/vendors/{vendor_id}/ vendor_code="updated vendor code" name="Updated Vendor Name" contact_details="Updated Contact Details" address="Updated Address" "Authorization: Token your_obtained_token"
#### PATCH method:
- http PATCH http://127.0.0.1:8000/api/vendor/{vendor_id}/ name="Updated Vendor Name"  address="Updated Address" "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint we have two commands with different http methods (PUT,PATCH).Here PUT handles updates by replacing the entire entity, so it creates a new entity. but where the PATCH handles by partial updating the given fields.

## Delete a vendor:
### using httpie:
- http DELETE http://127.0.0.1:8000/api/vendor/{vendor_id}/ "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to delete the vendor with given vendor_id.

## Create a purchase_order:
### using httpie:
- http POST http://127.0.0.1:8000/api/purchase_orders/ po_number="01" vendor=01 order_date="2023-01-01" delivery_date="2023-01-10" items='[{"item_name": 20 }]' quality_rating=4.5 issue_date="2023-01-01" status="Pending" acknowledgment_date="2023-01-02" "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to create a purchase_order with given details.

## List all purchase_orders details:
### using httpie:
- http http://127.0.0.1:8000/api/purchase_orders/ "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to get the details of all purchase_orders.

## Retrieve a specific purchase_order's details:
### using httpie:
- http http://127.0.0.1:8000/api/purchase_orders/{po_id}/ "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to get the details of purchase_order with given po_id.

## Update a purchase_order's details:
### using httpie:
#### PUT method:
- http PUT http://127.0.0.1:8000/api/purchase_orders/{po_id}/ po_number="UpdatedPO001" vendor="updatedid" order_date="2024-05-02" delivery_date="2024-05-15" items:='[{"item_name": 20 }]' quality_rating:=4.8 issue_date="2024-05-01" status="updated" acknowledgment_date="2024-05-02" "Authorization: Token your_obtained_token"
#### PATCH method:
- http PATCH http://127.0.0.1:8000/api/purchase_orders/{po_id}/ order_date="2024-05-02" items:='[{"item_name": "Updated Item", "quantity": 20 }]' quality_rating:=4.8 status="completed" "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint we have two commands with different http methods (PUT,PATCH).Here PUT handles updates by replacing the entire entity, so it creates a new entity. but where the PATCH handles by partial updating the given fields.

## Delete a purchase_order:
### using httpie:
- http DELETE http://127.0.0.1:8000/api/purchase_orders/{pk}/ "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to delete a purchase_order with given po_id.

## Retrieve a vendor's performance metrics:
### using httpie:
- http http://127.0.0.1:8000/api/vendors/{pk}/performance/ "Authorization: Token your_obtained_token"
### About this API endpoint:
- here this endpoint is used to retrieve the performance metrics of a vendor with given vendor_id. this performance metrics contains on_time Delivery rate, quality rating average, average response time, fulfilment rate
- On time delivery rate is calculated each time a PO status changes to "completed". this is the average of no of po delivered before the delivery_date and no of total po's delivered.
- quality rating average is calculated after every po completion and it is the average of all ratings given to that specific vendor.
- average response time is calculated each time a po is acknowledged by the vendor. it is the time difference between issue_date and acknowledgment_date for each po, and then the average of these times for all po's of the vendor.
- fulfillment rate is calculated when po status is set to "completed". this is the average of no of successfully fulfilled pos (status = "completed" without issues) by the total no of pos issued to the vendor.

## Update acknowledgment_data and trigger the recalculation of average_response_time:
### using httpie:
- http PATCH http://127.0.0.1:8000/api/purchase_orders/{pk}/acknowledge/ "Authorization: Token your_obtained_token" acknowledgment_date="2024-05-20"
### About this API endpoint:
- here this endpoint is used to acknowledge the purchase_order with given pk(primary key) and trigger the recalculation of average_reponse_time.Update to performance and vendor tabel.
