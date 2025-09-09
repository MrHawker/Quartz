# This is a drag and drop quantum circuit designer
Equipped with OPENQASM 3 generator and a simulator to sanity check design. Option to submit to IBM Qiskit Runtime is available as well
## Remember to download the depedencies
Listed in depedencies.txt
## To start the server
cd into the server folder and instantiate a virtual python env:
```
python -m .py.env .py.env
```
## To run the server
cd into the server folder and run 
```
.\.py.env\Scripts\activate.bat
python manage.py runserver 8000
```
## To exit the server
just run in the server folder
```
deactivate
```