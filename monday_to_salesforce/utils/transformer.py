def identity(x): return x
def join_labels(labels): return ';'.join([l.strip() for l in labels]) if isinstance(labels, list) else labels
def split_name(full_name):
    clean_name = " ".join(full_name.strip().split())
    
    if not clean_name:
        return ("Unknown", "")
    
    parts = clean_name.split(" ")
    if len(parts) == 1:
        return (parts[0], "")
    else:
        return (" ".join(parts[:-1]), parts[-1])

def get_added_and_removed_ids(event):
    new_ids = set([p['linkedPulseId'] for p in event['value'].get('linkedPulseIds', [])])
    old_ids = set([p['linkedPulseId'] for p in event.get('previousValue', {}).get('linkedPulseIds', [])])
    
    added_ids = set(new_ids) - set(old_ids)
    removed_ids = set(old_ids) - set(new_ids)
    
    return added_ids, removed_ids