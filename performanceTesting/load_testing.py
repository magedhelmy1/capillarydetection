from locust import HttpUser, task, constant
import json

class Request1(HttpUser):
    host = "http://127.0.0.1:8000/"

    @task
    def get_users(self):
        self.client.post("api/images/", data=
        {
            "backend_address": 1
        })

        # To check output is right
        # res = self.client.get("api/images/1")
        # response = json.loads(res.text)
        # print(response["capillary_area"])
