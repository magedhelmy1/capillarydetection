from ray import serve
import numpy as np
import requests
import os
import ray

"""
Part 0: Initialize Env to use CPU and ignore Ray reinitialization 
"""
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# ray.init(ignore_reinit_error=True)

"""
Part 1: Ray Serve Parameters
"""
# client = serve.start()
# config = {"num_replicas": 30}
# client.create_backend("tf:v1", TFMnistModel_RaySever, config=config)
# client.create_endpoint("tf_classifier", backend="tf:v1", route="/capServe")
# handle = client.get_handle("tf_classifier")

"""
Part 2 - Get Data from request and pass to server
"""


@serve.deployment(route_prefix="/mnist")
class TFMnistModel:
    def __init__(self, model_path):
        import tensorflow as tf
        self.model_path = model_path
        self.model = tf.keras.models.load_model(model_path)
        self.accuracy_accepted = 0.5

    async def __call__(self, starlette_request):
        # Step 1: transform HTTP request -> tensorflow input
        # Here we define the request schema to be a json array.
        input_array = np.array((await starlette_request.json())["array"])
        reshaped_array = input_array.reshape((1, 28, 28))

        # Step 2: tensorflow input -> tensorflow output
        prediction = self.model(reshaped_array)

        # Step 3: tensorflow output -> web output
        return {
            "prediction": prediction.numpy().tolist(),
            "file": self.model_path
        }


resp = requests.get(
    "http://localhost:8000/mnist",
    json={"array": np.random.randn(28 * 28).tolist()})
print(resp.json())
