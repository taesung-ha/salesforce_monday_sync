# connect_launcher.py
from config import CONNECTIONS
from monday_board_connecting import connect_items

print("🔗 Starting connect_launcher...", flush=True)

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

if __name__ == "__main__":
    connect_all_boards()
    print("✅ connect_launcher completed successfully!", flush=True)
