
from locust import FastHttpUser, task, between

class FileTransferUser(FastHttpUser):
    wait_time = between(0.5, 1)

    @task
    def download_file(self):
        with self.client.get(
            "/files?name=16kb.bin",
            name="GET /files (16KB)",
            catch_response=True,
            timeout=30
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"HTTP {response.status_code}"
                )
            elif response.content != b"A" * 16384:
                response.failure(
                    "File contents do not match"
                )
