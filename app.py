#Written by Adam Bishop
#ECE 4574
#Uses DynamoDB, AWS, and boto3. Pip to install those components

from __future__ import print_function # Python 2/3 compatibility
import argparse
import boto3
import sys
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# For a Boto3 client.
dynamodb = boto3.client('dynamodb',
						region_name='us-east-1', 
						endpoint_url='http://localhost:8001',
						aws_access_key_id='test',
						aws_secret_access_key='test'
						)

tablefetch = boto3.resource('dynamodb',
							region_name='us-east-1', 
							endpoint_url='http://localhost:8001',
							aws_access_key_id='test',
							aws_secret_access_key='test'
							)
						
#Deletes table specified by the -table arg						
def deleteTable( name ):
	table = dynamodb.delete_table(TableName=name)

#Queries using the year given in the -query arg	
def query( table, num ):
	year = str(num)

	response = dynamodb.query(
	TableName=table,
	KeyConditionExpression = '#y = :year',
	ExpressionAttributeNames = {
		'#y' : 'year'
	},
	ExpressionAttributeValues =  {
		':year' : {
			'N' : year
		}
	}
	)

	for i in response['Items']:
		print(i['year'], ":", i['title'])
		
def loadFromJSON( table, JSONname ):
	table = tablefetch.Table(table)
	with open(JSONname) as json_file:
		movies = json.load(json_file, parse_float = decimal.Decimal)
		for movie in movies:
			year = int(movie['year'])
			title = movie['title']
			info = movie['info']

			print("Adding movie:", year, title)

			table.put_item(
			   Item={
				   'year': year,
				   'title': title,
				   'info': info,
				}
			)

def createTable(tablename):
	table = table_fetch.create_table(
		TableName=tablename,
		KeySchema=[
			{
				'AttributeName': 'year',
				'KeyType': 'HASH'  #Partition key
			},
			{
				'AttributeName': 'title',
				'KeyType': 'RANGE'  #Sort key
			}
		],
		AttributeDefinitions=[
			{
				'AttributeName': 'year',
				'AttributeType': 'N'
			},
			{
				'AttributeName': 'title',
				'AttributeType': 'S'
			},

		],
		ProvisionedThroughput={
			'ReadCapacityUnits': 10,
			'WriteCapacityUnits': 10
		}
	)

	print("Table status:", table.table_status)
	
parser = argparse.ArgumentParser()

#Adds argument requirements/optionals
parser.add_argument('-table',
					action='store',
					help='Table Name',
					required=True,
					nargs=1)
					
parser.add_argument('-action',
					required=True,
					action='store',
					nargs=1,
					help='Action to perform',
					choices=['deleteTable','query','loadJSON','createTable'])
					
parser.add_argument('-query',
					action='store',
					nargs=1,
					help='year to be used with the query action')

parser.add_argument('-JSONname',
					action='store',
					nargs=1,
					help='name to be used with the loadJSON action')					

#Check args for syntax

args = parser.parse_args()
if args.action[0] == 'query' and args.query is None or len(args.query) != 1:
	parser.print_help()
	sys.exit()
elif args.action[0] == 'loadJSON' and args.JSONname is None:
	parser.print_help()
	sys.exit()
elif args.action[0] != 'query' and args.JSONname is not None:
	parser.print_help()
	sys.exit()
elif args.action[0] != 'loadJSON' and args.JSONname is not None:
	parser.print_help()
	sys.exit()


tableName = str(args.table[0])
JSONname = str(args.JSONname[0])
if len(tableName) < 3:
	print('Table name is too short')
	sys.exit()
	
if args.query is not None:
	year = int(args.query[0])

if args.action[0] == 'deleteTable':
	deleteTable(tableName)
elif args.action[0] == 'query':
	if type(year) is not int:
		print('Year must be an integer')
		sys.exit()
	else:
		query(tableName,year)
elif args.action[0] == 'createTable':
	createTable(tableName)
else:
	loadFromJSON(tableName,JSONname)
