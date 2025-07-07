import json
import os
from datetime import datetime, timedelta, timezone

sync_file = 'last_sync_time.txt'

def get_last_sync_time():
    if not os.path.exists(sync_file):
        print("No previous sync time found. Defaulting to 1000 days ago.")
        return (datetime.now(timezone.utc) - timedelta(days=1000)).isoformat()
    
    try:
        with open(sync_file, 'r') as f:
            data = json.load(f)
            return data.get('last_sync_time')
        
    except Exception as e:
        print(f"Error reading last sync time: {e}")
        return (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    
def save_sync_time():
    now = datetime.now(timezone.utc).isoformat()
    
    try:
        with open(sync_file, 'w') as f:
            json.dump({"last_sync_time": now}, f)
    except Exception as e:
        print(f'Error saving sync time: {e}')
        return
    
    '''
    # Git user 설정 (GitHub Actions용)
    os.system('git config --global user.name "github-actions[bot]"')
    os.system('git config --global user.email "github-actions[bot]@users.noreply.github.com"')

    # 변경 사항 스테이징
    os.system(f'git add {sync_file}')

    # 커밋 시도하고 결과 코드 확인
    commit_result = os.system('git commit -m "🔄 update last_sync_time"')
    print("🔍 git commit result:", commit_result)

    # push 시도하고 결과 코드 확인
    push_result = os.system('git push')
    print("🚀 git push result:", push_result)

    # 디버깅용 git 상태 확인
    os.system('git status')
    os.system('git log -1 --oneline')
    '''