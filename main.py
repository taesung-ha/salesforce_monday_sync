#%%
import os
from sync import sync_salesforce_to_monday
from sync_account import sync_account_records
from config import CONNECTIONS
from monday_board_connecting import connect_items

def sync_boards():
    board_configs = [
        "mapping_config/contact.json",
        "mapping_config/lead.json",
        "mapping_config/opportunity.json"
    ]

    for config_path in board_configs:
        print(f"\n🔄 Syncing board with config: {config_path}")
        try:
            sync_salesforce_to_monday(config_path)
            print(f"✅ Successfully synced board with config: {config_path}")
        except Exception as e:
            print(f"❌ Error syncing board with config {config_path}: {e}")
            print(f"Please check the configuration file and ensure all required fields are set correctly.")

    print("\n📦 Syncing Account board...")
    try:
        sync_account_records()
        print("✅ Successfully synced Account board.")
    except Exception as e:
        print(f"❌ Error syncing Account board: {e}")


def connect_all_boards():
    print("\n🔗 Starting Monday board linkage...")
    for conn in CONNECTIONS:
        print(f"\n=== ⛓ {conn['name']} 연결 시작 ===")
        try:
            connect_items(
                source_board_id=conn["source_board"],
                target_board_id=conn["target_board"],
                source_key_col_id=conn["source_col"],
                target_key_col_id=conn["target_col"],
                connect_col_id=conn["connect_col"]
            )
        except Exception as e:
            print(f"❌ Error in linking {conn['name']}: {e}")

def main():
    sync_boards()
    connect_all_boards()
    print("\n🔄 All boards synced and linked successfully!")
    
if __name__ == "__main__":
    main()