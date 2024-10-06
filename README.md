# Catalyst Count

Catalyst Count is a project designed to manage and process CSV file uploads with specific data requirements. This README provides instructions for setting up the project.

## Setup

Follow these steps to set up the project on your local machine.

### 1. Create a Virtual Environment

**For Linux:**

```bash
python3 -m venv env
source env/bin/activate   --> for linux 
.\env\Scripts\activate    --> for windows 


# install the requirements file 
pip install -r requirements.txt

python manage.py check

if everythig goes fine

run the server by  the  .sh 
make sure you are in the same directory in terminal wher .sh file is present 

chmod +x start_service.sh
./start_service.sh


now the server has started 

Note Steps to follow 

1) register a new user 
2) login with that user
3) make sure while uploadin the csv make sure the file structure must be same and the datatypes of the column must be same
else not you will encounter an error 
4) once the file is uploaded you can check the status of that file that is uploaded into db or not by 
checking the tab CSV file status 
5) if you see yes under the uploaded column you can filter the data 

Note: In the select option while filtering the options are generated on only 1000 records of the excel 
i think its just fot testing purpose that much data might be sufficient 


the excel will be shared in the email for your reference 




