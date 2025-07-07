# sync_launcher.py
import requests
from sync import sync_salesforce_to_monday
from sync_account import sync_account_records
from sync_utils import save_sync_time

print("🚀 Starting sync_launcher...", flush=True)

def sync_boards():
    board_configs = [
        "mapping_config/contact.json",
        "mapping_config/lead.json",
        "mapping_config/opportunity.json"
    ]

    for config_path in board_configs:
        print(f"\n🔄 Syncing board with config: {config_path}", flush=True)
        try:
            sync_salesforce_to_monday(config_path)
            print(f"✅ Successfully synced: {config_path}", flush=True)
        except Exception as e:
            print(f"❌ Error syncing {config_path}: {e}", flush=True)

    print("\n📦 Syncing Account board...", flush=True)
    try:
        sync_account_records()
        print("✅ Successfully synced Account board.", flush=True)
    except Exception as e:
        print(f"❌ Error syncing Account board: {e}", flush=True)

    save_sync_time()
    print("🕒 Sync time updated.", flush=True)


if __name__ == "__main__":
    sync_boards()
    print("✅ sync_launcher completed successfully!", flush=True)
