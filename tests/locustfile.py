from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        payload = {"email": "admin@irontemple.com"}
        self.client.post("/showSummary", data=payload)

    @task
    def purchase_places(self):
        payload = {
            "places": 1,
            "club": "Iron Temple",
            "competition": "Winter 2024",
        }
        self.client.post("/purchasePlaces", data=payload)
