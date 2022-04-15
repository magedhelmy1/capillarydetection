from locust import HttpUser, task


class TestImage(HttpUser):
    host = "http://164.90.191.198/"

    @task
    def post_images(self):
        self.client.post(url="api/analyze_im/")
