import factory

from project import models


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    title = factory.Faker("name")
    user = None
