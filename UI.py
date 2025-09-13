
stub_path = 'stubs/stats.pkl'
if stub_path is not None and os.path.exists(stub_path):
    with open(stub_path,'rb') as f:
        stats = pickle.load(f)