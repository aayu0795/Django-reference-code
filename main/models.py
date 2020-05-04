from django.db import models
from django.db.models.signals import post_save
from datetime import timedelta


class PersonQueryset(models.QuerySet):
    """
    A QuerySet represents a collection of objects from your database.
    """

    def male(self):
        return self.filter(gender="M")


class PersonManager(models.Manager):
    """
    A Manager is the interface through which
    database query operations are provided to Django models.
    """

    def get_queryset(self):
        return super().get_queryset()

    def male(self):
        return self.get_queryset().filter(gender="M")

    def female(self):
        return self.get_queryset().filter(gender="F")

    def other(self):
        return self.get_queryset().filter(gender="O")

    # # Making use of our own queryset
    # def get_queryset(self):
    #     # self.model define the table and using define the reference to the database
    #     return PersonQueryset(self.model, using=self._db)

    # # By "Person.objects.male()" we can use our custom queryset
    # def male(self):
    #     return self.get_queryset().male()


GENDER = {
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
}


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()

    # Creating choices field
    gender = models.CharField(choices=GENDER, max_length=1)
    cars = models.ManyToManyField('Car')

    objects = PersonManager()

    class Meta:
        ordering = ["first_name"]
        verbose_name_plural = "Person's"

    def __str__(self):
        return self.first_name

    @property
    def has_passport(self):
        return Passport.objects.filter(person=self).exists()

    @property
    def owned_cars(self):
        return self.cars.all()

    @property
    def owned_houses(self):
        return self.house_set.all()


class Passport(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    passport_id = models.CharField(max_length=8)
    issue_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField(auto_now_add=True)
    country = models.CharField(max_length=50)

    class Meta:
        ordering = ["passport_id"]
        verbose_name_plural = "Passport's"

    def __str__(self):
        return self.person.first_name

    def save(self, *args, **kwargs):    # Overriding the default save method
        # Do_something
        super().save(*args, **kwargs)  # Call the "real" save() method.


# Signal reciever function
def update_passport_expiry_date(sender, instance, **kwargs):
    instance.expire_date += timedelta(days=1825)


# Update the Expire date of passport by 5 year once the post_save signal is received
post_save.connect(update_passport_expiry_date, sender=Passport)


class Car(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Car's"

    def __str__(self):
        return self.name


class House(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    house_no = models.IntegerField()
    landmark = models.CharField(max_length=60)
    address = models.CharField(max_length=100)

    class Meta:
        ordering = ["house_no", "landmark", "address"]

    def __str__(self):
        return self.person.first_name
