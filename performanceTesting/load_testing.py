from locust import HttpUser, task, constant


class TestImage(HttpUser):
    host = "http://64.227.106.224/"

    # host = "http://127.0.0.1/"

    @task
    def post_images(self):
        # self.client.get(url="api/example/")
        self.client.post(url="api/analyze_im/")
        # self.client.post("nginx_hello")
