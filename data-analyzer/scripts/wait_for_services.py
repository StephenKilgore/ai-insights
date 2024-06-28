import time
import socket

def wait_for_service(host, port, timeout=60):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=5):
                return True
        except (OSError, socket.error):
            if time.time() - start_time >= timeout:
                return False
            time.sleep(2)

if __name__ == "__main__":
    rabbitmq_ready = wait_for_service("ai-insights-rabbitmq", 5672)
    postgres_ready = wait_for_service("ai-insights-db", 5432)

    if rabbitmq_ready and postgres_ready:
        print("All services are ready!")
    else:
        print("Some services are not available. Exiting.")
        exit(1)
