#!/usr/bin/env python

from locust import HttpLocust, TaskSet, task

"""
def login(l):
    l.client.post("/login", {"username":"ellen_key", "password":"education"})


def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {index:2, profile:1}

    def on_start(self):
        login(self)

"""

class MyTaskSet(TaskSet):
        @task
        def my_task(self):
                self.client.get("/testapi?image_size=hdpi&type_1=cricket&search=james")



class Remote(TaskSet):
        @task
        def remote_task(self):
            self.client.post("/geteatery", {"__eatery_id": "0b1c923608da1ed74c521da4d1ff6f66cc329279a618f091e549d5df1585fb2e"}) 



class NewsApi(TaskSet):
        @task
        def mixed_api(self):
                self.client.get("/mixed?skip=10&image_size=hdpi&limit=10&type_1=cricket")






class MyLocust(HttpLocust):
    task_set = MyTaskSet

