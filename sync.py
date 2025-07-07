import json
from config import get_envs

from salesforce import get_salesforce_access_token, fetch_salesforce_records
from monday import get_monday_items, create_or_update_monday_item
from sync_utils import get_last_sync_time

env = get_envs()


def sync_salesforce_to_monday(board_config_path):
    with open(board_config_path) as f:
        config = json.load(f)

    monday_board_id = config["board_id"]
    salesforce_column_id = config["salesforce_id_column_id"]
    salesforce_select_fields = config.get("salesforce_select_fields", "*")
    salesforce_object = config["salesforce_object"]
    salesforce_condition = config.get("salesforce_condition", None)
    salesforce_condition2 = config.get("salesforce_condition2", None)
    field_mapping = config["field_mapping"]

    if not all([SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD, MONDAY_TOKEN, monday_board_id]):
        print("Missing configuration for Salesforce or Monday.com.")
        return

    access_token, instance_url = get_salesforce_access_token(SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD)

    if not access_token or not instance_url:
        print("Failed to authenticate with Salesforce.")
        return

    print("Access Token:", access_token)
    print("Instance URL:", instance_url)
    print("Salesforce authentication complete.")

    last_sync = get_last_sync_time()

    records = fetch_salesforce_records(
        instance_url = instance_url, 
        access_token = access_token, 
        object_name = salesforce_object, 
        select_fields = salesforce_select_fields, 
        conditions = salesforce_condition,
        from_datetime = last_sync
    )

    if not records:
        print("No new records found in Salesforce.")
        return

    if salesforce_condition2: #when salesforce_condition2 is not None, it means that the user wants to fetch records with two conditions. they are combined with OR operator
        records2 = fetch_salesforce_records(
            instance_url = instance_url, 
            access_token = access_token, 
            object_name = salesforce_object, 
            select_fields = salesforce_select_fields, 
            conditions = salesforce_condition2,
            from_datetime = last_sync
        )

        records.extend(records2)
        unique_records = {}

        for record in records:
            unique_records[record['Id']] = record

        records = list(unique_records.values())

    monday_items = get_monday_items(monday_board_id, MONDAY_TOKEN, salesforce_column_id)
    if not monday_items:
        print("No items found in Monday.com. Creating new items.")

    for record in records:
        create_or_update_monday_item(record, monday_items, monday_board_id, MONDAY_TOKEN, field_mapping)

    print(f"Successfully synced {len(records)} records to Monday.com.")