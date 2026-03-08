#!/usr/bin/env python3
"""
DynamoDB Tables Setup for Hotel Booking System
Run this once to initialize all DynamoDB tables
"""

import boto3
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))

def create_users_table():
    """Create Users table"""
    try:
        table = dynamodb.create_table(
            TableName=os.getenv('AWS_DYNAMODB_TABLE_USERS', 'hotel_users'),
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email-index',
                    'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # Serverless pricing
        )
        print(f"✓ Users table created: {table.table_name}")
        return True
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("✓ Users table already exists")
        return True
    except Exception as e:
        print(f"✗ Error creating Users table: {e}")
        return False

def create_rooms_table():
    """Create Rooms table"""
    try:
        table = dynamodb.create_table(
            TableName=os.getenv('AWS_DYNAMODB_TABLE_ROOMS', 'hotel_rooms'),
            KeySchema=[
                {'AttributeName': 'room_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'room_id', 'AttributeType': 'N'},
                {'AttributeName': 'room_type', 'AttributeType': 'S'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'room_type-index',
                    'KeySchema': [{'AttributeName': 'room_type', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"✓ Rooms table created: {table.table_name}")
        return True
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("✓ Rooms table already exists")
        return True
    except Exception as e:
        print(f"✗ Error creating Rooms table: {e}")
        return False

def create_bookings_table():
    """Create Bookings table"""
    try:
        table = dynamodb.create_table(
            TableName=os.getenv('AWS_DYNAMODB_TABLE_BOOKINGS', 'hotel_bookings'),
            KeySchema=[
                {'AttributeName': 'booking_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'booking_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'check_in', 'AttributeType': 'S'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id-index',
                    'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                },
                {
                    'IndexName': 'check_in-index',
                    'KeySchema': [{'AttributeName': 'check_in', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"✓ Bookings table created: {table.table_name}")
        return True
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("✓ Bookings table already exists")
        return True
    except Exception as e:
        print(f"✗ Error creating Bookings table: {e}")
        return False

def create_reviews_table():
    """Create Reviews table"""
    try:
        table = dynamodb.create_table(
            TableName=os.getenv('AWS_DYNAMODB_TABLE_REVIEWS', 'hotel_reviews'),
            KeySchema=[
                {'AttributeName': 'review_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'review_id', 'AttributeType': 'S'},
                {'AttributeName': 'room_id', 'AttributeType': 'N'},
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'room_id-index',
                    'KeySchema': [{'AttributeName': 'room_id', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"✓ Reviews table created: {table.table_name}")
        return True
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("✓ Reviews table already exists")
        return True
    except Exception as e:
        print(f"✗ Error creating Reviews table: {e}")
        return False

def main():
    print("="*60)
    print("DynamoDB Tables Setup")
    print("="*60 + "\n")
    
    tables = [
        ("Users", create_users_table),
        ("Rooms", create_rooms_table),
        ("Bookings", create_bookings_table),
        ("Reviews", create_reviews_table),
    ]
    
    results = []
    for name, func in tables:
        results.append(func())
    
    print("\n" + "="*60)
    if all(results):
        print("✓ All DynamoDB tables initialized successfully!")
    else:
        print("✗ Some tables failed to create")
    print("="*60)

if __name__ == "__main__":
    main()
