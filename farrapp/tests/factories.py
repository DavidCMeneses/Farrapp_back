import factory
import pytest
from faker import Faker
from api.models import ClientModel, Category, Schedule, EstablishmentModel, Rating

fake = Faker()

class CategoryFactory (factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = factory.Sequence(lambda n: "Category %d" % n)
    type = factory.LazyFunction(lambda: fake.random_choices(elements=('M','E'), length=1)[0])

class ScheduleFactory (factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule
    
    open = factory.LazyFunction(lambda: fake.date_time())
    close = factory.LazyFunction(lambda: fake.date_time())
    day = factory.Sequence(lambda n: "Category %d" % n)

class DemoClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientModel
    
    username = "chamber"
    email = "siuu@gmail.com"
    first_name = "que"
    last_name = "so"
    birthday = "2001-01-01"
    sex = 'F'

class ClientModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientModel

    username = factory.Sequence(lambda n: "User %d" % n)
    email = factory.LazyAttribute(lambda obj: "%s@gmail.com" % obj.username)
    first_name = factory.LazyFunction(lambda: fake.name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    birthday = factory.LazyFunction(lambda: fake.date())
    sex = 'F'

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)

        else:
            categories = CategoryFactory.create_batch(5)
            for category in categories:
                self.categories.add(category)
        


class EstablishmentModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EstablishmentModel
    
    username = factory.Sequence(lambda n: "User %d" % (n + 100000))
    email = factory.LazyAttribute(lambda obj: "%s@gmail.com" % obj.username)
    name = factory.LazyFunction(lambda: fake.name())
    address = factory.LazyFunction(lambda: fake.address())
    city = factory.LazyFunction(lambda: fake.city())
    country = factory.LazyFunction(lambda: fake.country())
    description = "Un tomadero como cualquier otro"
    rut = 11111
    verified = False
    playlist_id = "https://github.com/DavidCMeneses/Farrapp_back"
      
    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)

        else:
            categories = CategoryFactory.create_batch(5)
            for category in categories:
                self.categories.add(category)

    @factory.post_generation
    def schedules(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for schedule in extracted:
                self.schedules.add(schedule)

        else:
            schedules = ScheduleFactory.create_batch(3)
            for schedule in schedules:
                self.schedules.add(schedule)

class RatingFactory (factory.django.DjangoModelFactory):
    class Meta:
        model = Rating
    
    stars = factory.LazyFunction(lambda: fake.random_int(min=0, max=5))
    client = factory.SubFactory(ClientModelFactory)
    establishment = factory.SubFactory(EstablishmentModelFactory)
