from locust import HttpUser, task


class TestImage(HttpUser):
    # host = "http://64.227.106.224/"
    # host = "http://127.0.0.1/"
    host = "http://139.59.206.141/"

    @task
    def post_images(self):
        # self.client.get(url="api/example/")
        # self.client.post(url="api/hello")
        self.client.post(url="api/analyze_im/")
        # self.client.post("nginx_hello")
        # self.client.post("api/performance_test/")
