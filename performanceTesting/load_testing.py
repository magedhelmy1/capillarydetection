from locust import HttpUser, task, constant


class Request1(HttpUser):
    host = "http://127.0.0.1:8000"

    @task
    def get_users(self):
        res = self.client.get("/")
        print(res.status_code)
