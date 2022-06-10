# coding: utf8
from app import models as m


class TasksRepository(object):
    def create(self, **kwargs):
        tasks = m.Tasks(task=kwargs.get("task"))
        tasks.save()
        return tasks


tasks_repo = TasksRepository()
