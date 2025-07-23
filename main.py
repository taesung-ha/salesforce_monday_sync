print("🎯 main.py Implemented!", flush=True)
#%%
from sync import sync_salesforce_to_monday
from sync_account import sync_account_records
from config import CONNECTIONS
from monday_board_connecting import connect_items
from sync_utils import save_sync_time

def sync_boards():
    board_configs = [
        "mapping_config/opportunity.json",
        "mapping_config/contact.json",
        "mapping_config/lead.json"
    ]

    for config_path in board_configs:
        print(f"\n🔄 Syncing board with config: {config_path}", flush=True)
        try:
            sync_salesforce_to_monday(config_path)
            print(f"✅ Successfully synced board with config: {config_path}", flush=True)
        except Exception as e:
            print(f"❌ Error syncing board with config {config_path}: {e}", flush=True)
            print(f"Please check the configuration file and ensure all required fields are set correctly.", flush=True)

    print("\n📦 Syncing Account board...")
    
    try:
        sync_account_records()
        print("✅ Successfully synced Account board.", flush=True)
    except Exception as e:
        print(f"❌ Error syncing Account board: {e}", flush=True)

def connect_all_boards():
    print("\n🔗 Starting Monday board linkage...")
    for conn in CONNECTIONS:
        print(f"\n=== ⛓ {conn['name']} Start linking the boards ===", flush=True)
        try:
            connect_items(
                source_board_id=conn["source_board"],
                target_board_id=conn["target_board"],
                source_key_col_id=conn["source_col"],
                target_key_col_id=conn["target_col"],
                connect_col_id=conn["connect_col"]
            )
        except Exception as e:
            print(f"❌ Error in linking {conn['name']}: {e}", flush=True)

def main():
    sync_boards()
    
    #save_sync_time()
    print("📝 Sync time updated.")
    connect_all_boards()
    print("\n🔄 All boards synced and linked successfully!", flush=True)
    
    print("🎉 Process completed successfully!", flush=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "sync":
            sync_boards()
            #save_sync_time()
        elif mode == "link":
            connect_all_boards()
        elif mode == "all":
            main()
        else:
            print("❌ Unknown mode. Use: sync | link | all")
    else:
        main()