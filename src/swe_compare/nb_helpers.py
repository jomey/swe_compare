from dask.distributed import Client

def start_cluster(n_workers=10, memory_limit='4GB'):
    cluster = Client(
        n_workers=n_workers, 
        threads_per_worker=1, 
        memory_limit=memory_limit
    )
    print(cluster.dashboard_link)
    return cluster
    