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

def get_newly_linked_ids(event):
    new_ids = set([p['linkedPulseId'] for p in event['value'].get('linkedPulseIds', [])])
    old_ids = set([p['linkedPulseId'] for p in event.get('previousValue', {}).get('linkedPulseIds', [])])
    return list(new_ids - old_ids)