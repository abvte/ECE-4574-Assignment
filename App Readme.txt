By Adam Bishop
For ECE 4574

This is an application that works with the local DynamoDB that is in the same folder as the application
The database holds 5000 or so movie titles and dates for them in a table names "Movies" (only table in the database)
The application is a command line interface that allows the user to query the table based on the year the movie came out, and also allows the user to delete the table

----------------------------------Requirements------------------------------------

Download the latest version of Python

Then

Using pip, download using these commands:

pip install boto3
pip install awscli

If you find that every query asks for credentials in the terminal type this:

aws configure

Type anything in for when it prompts you. Your credentials don't matter for local DynamoDB but they have to exist

----------------------------------Start database----------------------------------

Before anything, go to the directory of the DynamoDb install, start the terminal then type:

java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 8001

This will start the database and allow it to be queried. Exit it with ctrl-C

If port 8001 doesn't work, feel free to change it

----------------------------------Usage-------------------------------------------

usage: app.py [-h] -table TABLE -action {deleteTable,query} [-query QUERY]

optional arguments:
  -h, --help            show this help message and exit
  -table TABLE          Table Name 
  -action {deleteTable,query}
                        Action to perform
  -query YEAR          year to be used with the query action

----------------------------------Usage Examples----------------------------------

Examples (There is only one table! "Movies" is the table name, so your input should always be "Movies" without quotes):

Delete - 
	python app.py -table Movies -action deleteTable
	
Query (will only return movies that released in 2000)-
	python app.py -table Movies -action query -query 2000
	
Notice that Query is needed to be specified in the action argument and needed an extra argument (-query) to specify the year 