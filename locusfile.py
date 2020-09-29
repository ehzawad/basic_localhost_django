from locust import User, HttpUser, TaskSet, task, between
import logging
import gevent
import time
from locust import events
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, WorkerRunner

@events.test_start.add_listener
def on_test_start(**kwargs):
    print("A new test is starting")

# adjust your routes and write task accordingly
class MyTasks(TaskSet):
    @task(2)
    def load_user_profile(self):
        self.client.get("/polls")
        # self.client.get("/admin")
    @task(1)
    def load_admin_profile(self):
        self.client.get("/admin")

    wait_time = between(5, 15)

class MyWebsiteUser(HttpUser):
    tasks = [MyTasks]


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print("A new test is ending")


@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0




def checker(environment):
    while not environment.runner.state in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
        time.sleep(1)
        if environment.runner.stats.total.fail_ratio > 0.2:
            print(f"fail ratio was {environment.runner.stats.total.fail_ratio}, quitting")
            environment.runner.quit()
            return


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    # only run this on master & standalone
    if not isinstance(environment.runner, WorkerRunner):
        gevent.spawn(checker, environment)
