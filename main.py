import os
from sync import sync_salesforce_to_monday
from sync_account import sync_account_records

def main():
    board_configs = [
        "mapping_config/contact.json",
        "mapping_config/lead.json",
        "mapping_config/opportunity.json",
    ]
    
    for config_path in board_configs:
        print(f"Syncing board with config: {config_path}")
        try:
            sync_salesforce_to_monday(config_path)
            print(f"✅ Successfully synced board with config: {config_path}")
        except Exception as e:
            print(f"❌ Error syncing board with config {config_path}: {e}")
            print(f"Please check the configuration file and ensure all required fields are set correctly.")
            # Account board는 별도 처리
            
    print("\n📦 Syncing Account board...")
    try:
        sync_account_records()
        print("✅ Successfully synced Account board.")
    except Exception as e:
        print(f"❌ Error syncing Account board: {e}")
if __name__ == "__main__":
    main()