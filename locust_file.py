from locust import HttpLocust, TaskSet, task


class TestApi(TaskSet):
#    def on_start(self):
#        print 'INSIDE START'
#        self.mixed_task()

    @task
    def mixed_task(self):
        print 'INSIDE MIXD TASK'
        response = self.client.get('/mixed?image_size=ldpi')
        print 'RESPONSE::::::::', response


class LocustClass(HttpLocust):
    task_set = TestApi
