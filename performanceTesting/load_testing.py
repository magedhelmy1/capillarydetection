from locust import HttpUser, task, constant


class TestImage(HttpUser):
    host = "http://127.0.0.1/"

    @task
    def get_users(self):
        self.client.post(url="api/analyze_im/")
