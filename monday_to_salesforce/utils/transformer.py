def identity(x): return x
def join_labels(labels): return ';'.join([l.strip() for l in labels]) if isinstance(labels, list) else labels