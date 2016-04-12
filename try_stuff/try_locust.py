#!/usr/bin/env python


from locust import Locust, HttpLocust ,TaskSet, task

class MyTaskSet(TaskSet):
    @task
    def my_task(self):
        print "executing my_task"
        response = self.client.get('http://localhost:8000/v1/get_match_list')
        

class MyLocust(HttpLocust):
    task_set = MyTaskSet
