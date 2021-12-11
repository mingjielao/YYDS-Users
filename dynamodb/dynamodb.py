import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from datetime import datetime
import time
import uuid

# There is some weird stuff in DynamoDB JSON responses. These utils work better.
# I am not using  in this example.
# from dynamodb_json import json_util as jsond

# There are a couple of types of client.
# I create both because I like operations from both of them.
#
# I comment out the key information because I am getting this from
# my ~/.aws/credentials files. Normally this comes from a secrets vault
# or the environment.
#
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="AKIA3G2MEQCFDAHOJZUX",
                          aws_secret_access_key="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",
                          region_name='us-east-2')

other_client = boto3.client("dynamodb", region_name='us-east-2')

'''
eg. in User-Event Table
get_attribute_list("User-Event", "user_id", "event_id", 25)

this will return all event_id that user 25 joined
'''
def get_attribute_set(table_name, attribute_key_name, attribute_to_get_name, attribute_key_value):
    res = get_item(table_name,
                      {
                          attribute_key_name: attribute_key_value
                      })
    if res:
        return res[attribute_to_get_name]
    else:
        return res

'''
eg. in User-Event Table
add_attribute("User-Event", "user_id", "event_id", 25, 9)

if user 25 exists in the table, this will add 9 to the event id list of user 25
If user 25 does not exist in the table, this will create a row with user 25 and add 9 to the event id list of this newly created user
'''
def add_relation(table_name, attribute_name1, attribute_name2, attribute_value1, attribute_value2):
    if find_by_attribute(table_name, attribute_name1, attribute_value1):
        res = add_attribute(table_name, attribute_name1, attribute_name2, attribute_value1, attribute_value2)
    else:
        l = {attribute_value2}
        item = {
            attribute_name1: attribute_value1,
            attribute_name2: l,
            "version_id": str(uuid.uuid4()),
        }

        res = put_item(table_name, item=item)
    return res


'''
eg. in User-Event Table
remove_attribute("User-Event", "user_id", "event_id", 25, 9)

if user 25 exists in the table, this will remove 9 from the event id list of user 25
If user 25 does not exist in the table, this doesn't do anything
'''
def remove_relation(table_name, attribute_name1, attribute_name2, attribute_value1, attribute_value2):
    res = remove_attribute(table_name, attribute_name1, attribute_name2, attribute_value1, attribute_value2)
    return res





















def remove_attribute(table_name, attribute_key_name, attribute_to_add_name, attribute_key_value, attribute_to_add_value):
    table = dynamodb.Table(table_name)
    Key = {
        attribute_key_name: attribute_key_value
    }
    UpdateExpression = "DELETE " + attribute_to_add_name + " :c"
    ExpressionAttributeValues = {
        ":c": {attribute_to_add_value }
    }
    ReturnValues = "UPDATED_NEW"

    res = table.update_item(
        Key=Key,
        UpdateExpression=UpdateExpression,
        ExpressionAttributeValues=ExpressionAttributeValues,
        ReturnValues=ReturnValues
    )

    return res


def add_attribute(table_name, attribute_key_name, attribute_to_add_name, attribute_key_value, attribute_to_add_value):
    table = dynamodb.Table(table_name)
    Key = {
        attribute_key_name: attribute_key_value
    }
    UpdateExpression = "ADD " + attribute_to_add_name + " :c"
    ExpressionAttributeValues = {
        ":c": {attribute_to_add_value }
    }
    ReturnValues = "UPDATED_NEW"

    res = table.update_item(
        Key=Key,
        UpdateExpression=UpdateExpression,
        ExpressionAttributeValues=ExpressionAttributeValues,
        ReturnValues=ReturnValues
    )

    return res

def get_item(table_name, key_value):
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key=key_value
    )

    response = response.get('Item', None)
    return response


def put_item(table_name, item):
    table = dynamodb.Table(table_name)
    res = table.put_item(Item=item)
    return res


# primiary key -> attribute1



def find_by_attribute(table_name, attribute_name, attribute_value):
    table = dynamodb.Table(table_name)

    expressionAttributes = dict()
    expressionAttributes[":S"] = attribute_value
    filterExpression = "contains(" + attribute_name + ", :S)"

    result = table.scan(FilterExpression=filterExpression,
                        ExpressionAttributeValues=expressionAttributes)
    #json.dumps(result, indent=3)
    return result["Items"]


def write_relation_if_not_changed(tabale_name, new_relation, old_relation):
    new_version_id = str(uuid.uuid4())
    new_relation["version_id"] = new_version_id

    old_version_id = old_relation["version_id"]

    table = dynamodb.Table(tabale_name)

    res = table.put_item(
        Item=new_relation,
        ConditionExpression="version_id=:old_version_id",
        ExpressionAttributeValues={":old_version_id": old_version_id}
    )

    return res
