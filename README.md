
# Hospital Management System


Welcome to our Hospital Management System! This project aims to streamline and optimize the administrative and operational processes within a healthcare facilities. It list down information of registered Hospitals as well listing Patients credentials.



## Setup

- The first thing to do is to clone the repository

```
 $ git clone https://github.com/sa3640/hospital_management_system.git
```

- Now create a Virtual Environment

```
py -m venv virtual name
```

- Activate Virtual Environment

```
  source hospital/Scripts/activate
```

- Install all the Dependencies

```
 pip install -r requirement.txt
```

- Move to the Project Directory

```
 cd hospital_management_system
```

- Run the Server

```
py manage.py runserver
```

- Navigate the Project On Web Browser

```
http://127.0.0.1:8000/
```
## API Reference

#### User Signup 

```http
http://127.0.0.1:8000/signup/
```

#### User Login 

```http
http://127.0.0.1:8000/login/
```


#### Get all Patients

```http
  http://127.0.0.1:8000/patient/
```



#### Get all Hospitals

```http
  http://127.0.0.1:8000/hospitals/
```



#### Get all Patients visits


```http
http://127.0.0.1:8000/patientvisit/
```