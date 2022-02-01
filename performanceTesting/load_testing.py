from locust import HttpUser, task


class TestImage(HttpUser):
    host = "http://139.59.206.141/"

    @task
    def post_images(self):
        self.client.post(url="api/analyze_im/")
