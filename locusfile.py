from locust import User, HttpUser, TaskSet, task, between

class MyTasks(TaskSet):
    @task
    def load_user_profile(self):
        self.client.get("/polls")

    wait_time = between(5, 15)

class MyWebsiteUser(HttpUser):
    tasks = [MyTasks]
