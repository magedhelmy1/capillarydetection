from locust import HttpUser, task, constant


class Request1(HttpUser):
    host = "http://64.227.106.224/"
    wait_time = constant(1)

    @task
    def get_users(self):
        res = self.client.get("/api/users?page=2")
        print(res.text)
        print(res.status_code)
        print(res.headers)
