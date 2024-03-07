import threading
POOL_SIZE = 10
# Define the thread pool
thread_pool = []

# Accept incoming connections and handle them with the thread pool
if len(thread_pool) < POOL_SIZE:
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread_pool.append(thread)
        thread.start()
else:
        # Wait for an available thread in the pool
        for thread in thread_pool:
            if not thread.is_alive():
                thread_pool.remove(thread)
                thread = threading.Thread(target=handle_client, args=(client_socket, address))
                thread_pool.append(thread)
                thread.start()
                break
