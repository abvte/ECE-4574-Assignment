# Written by Adam Bishop
# ECE 4574
# Uses DynamoDB, AWS, and boto3. Pip to install those components

from __future__ import print_function  # Python 2/3 compatibility
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

# Deletes table specified by the -table arg


def deleteTable(name):
    table = dynamodb.delete_table(TableName=name)

# Queries using the year given in the -query arg


def query(table, num):
    year = str(num)

    response = dynamodb.query(
        TableName=table,
        KeyConditionExpression='#y = :year',
        ExpressionAttributeNames={
            '#y': 'year'
        },
        ExpressionAttributeValues={
            ':year': {
                'N': year
            }
        }
    )

    for i in response['Items']:
        print(i['year'], ":", i['title'], ":", i['info']['M']['rating'])


def putItem(tableName):
    table = tablefetch.Table(tableName)
    title = raw_input('Enter Movie Title- ')
    year = input('Enter year of release- ')
    rating = input('Enter rating- ')
    response = table.put_item(
        Item={
            'year': year,
            'title': title,
            'info': {
                'plot': 'Something happens.',
                'rating': rating
            }
        }
    )

    print("PutItem succeeded:")


def updateItem(tableName):
    table = tablefetch.Table(tableName)
    title = raw_input('Enter Movie Title- ')
    year = input('Enter year of release- ')
    newRating = input('Enter new Rating of Movie- ')
    response = table.update_item(
        Key={
            'year': year,
            'title': title
        },
        UpdateExpression="set info.rating = :r",
        ExpressionAttributeValues={
            ':r': decimal.Decimal(newRating)
        },
        ReturnValues="UPDATED_NEW"
    )

    print("PutItem succeeded:")


def deleteItem(tableName):
    table = tablefetch.Table(tableName)
    title = raw_input('Enter Movie Title- ')
    year = input('Enter year of release- ')
    response = table.delete_item(
        Key={
            'year': year,
            'title': title
        }
    )
    print("DeleteItem succeeded:")


def loadFromJSON(table, JSONname):
    table = tablefetch.Table(table)
    with open(JSONname) as json_file:
        movies = json.load(json_file, parse_float=decimal.Decimal)
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
    table = tablefetch.create_table(
        TableName=tablename,
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
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

# Adds argument requirements/optionals
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
                    choices=['deleteTable', 'query', 'loadJSON', 'createTable', 'putItem', 'updateItem', 'deleteItem'])

parser.add_argument('-query',
                    action='store',
                    nargs=1,
                    help='year to be used with the query action')

parser.add_argument('-JSONname',
                    action='store',
                    nargs=1,
                    help='name to be used with the loadJSON action')

# Check args for syntax
args = parser.parse_args()

# handle table arg
if args.table[0] is None:
    print('Table name not provided')
    sys.exit()
else:
    tableName = str(args.table[0])
    if len(tableName) < 3:
        print('Table name too short')
        sys.exit()

# handling action arg
if args.action[0] == 'query':
    if args.query is None or len(args.query) != 1:
        parser.print_help()
        sys.exit()
    else:
        year = int(args.query[0])
        if(year <= 0):
            print('Year must be non negative integer')
            sys.exit()
        else:
            query(tableName, year)
elif args.action[0] == 'loadJSON':
    if args.JSONname is None:
        parser.print_help()
        sys.exit()
    else:
        JSONname = str(args.JSONname[0])
        loadFromJSON(tableName, JSONname)
elif args.action[0] == 'deleteTable':
    deleteTable(tableName)
elif args.action[0] == 'createTable':
    createTable(tableName)
elif args.action[0] == 'putItem':
    putItem(tableName)
elif args.action[0] == 'updateItem':
    updateItem(tableName)
elif args.action[0] == 'deleteItem':
    deleteItem(tableName)
