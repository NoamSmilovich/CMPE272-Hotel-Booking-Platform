# CMPE272 Hotel Booking Platform
## Setup Information
The setup was tested on an M1 Mac running MacOS Ventura 13.2.1.
### Pre-requisites
* Java JDK 17 
* MySQL 8.0.30
* MySQL Workbench 8.0.29 or higher
* Python 3.9 or higher
It is crucial to have the exact specifications above. Java server testing on Java JDK 20 failed.
### Setup
1. Clone the GitHub repository to the desired folder using the following command: 

```
git clone https://github.com/NoamSmilovich/CMPE272-Hotel-Booking-Platform.git
```

2. In order to set a virtual environment, installation of virtualenv platform is required. This is not mandatory, but it is recommended.
Use the following commands to create a new working virtual environment with all the required dependencies:

```
cd CMPE272-Hotel-Booking-Platform/PythonClient
python -m virtualenv .
.\Scripts\activate
pip install -r requirements.txt
```

3. Navigate to the JavaServer folder and run the following commands to start the server:

```
java -cp .:"Dependencies/*.jar" -jar javaserver.jar
```

4. Navigate to the PythonClient folder and run the following commands to start the client:

```
python GUI.py
```

Now the GUI should start, and you can explore the functionality of the application. Note that the GUI will not start if the server is not running first. 

**Important:** you will not be able to explore the functionality of the MySQL portion unless you start a local MySQL server and run the ‘hotels_mock_data.sql’ script in the main folder first.
