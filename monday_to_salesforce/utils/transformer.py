def identity(x): return x
def join_labels(labels): return ';'.join([l.strip() for l in labels]) if isinstance(labels, list) else labels
def split_name(full_name):
    parts = full_name.strip().split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else "Unknown"
    return first_name, last_name
