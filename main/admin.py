from django.contrib import admin
from .models import Car, House, Passport, Person
from datetime import timedelta


def increase_expiry_date(modeladmin, request, queryset):
    new_expiry_date = queryset[0].expire_date + timedelta(days=1825)
    queryset.update(expire_date=new_expiry_date)


# `short_description` is used to show the custom action in action dropdown field
increase_expiry_date.short_description = "Increase expire date by 5 year"


def decrease_expiry_date(modeladmin, request, queryset):
    new_expiry_date = queryset[0].expire_date - timedelta(days=1825)
    queryset.update(expire_date=new_expiry_date)


# `short_description` is used to show the custom action in action dropdown field
decrease_expiry_date.short_description = "Decrease expire date by 5 year"


class PersonAdmin(admin.ModelAdmin):
    # list_d`isplay allow us to show fields model list view
    list_display = ['first_name', 'last_name', 'age', 'gender', 'full_name']

    # `fields` allow us to define models fields to be shown during edit/create
    fields = ['first_name', 'last_name', 'age', 'gender', 'cars']

    # `list_display_link` allow us to redirect to the model list view
    # to use this, fields must be present in list_display
    list_display_links = ['first_name']

    # `list_editable` all us to edit field directly from model list view
    list_editable = ['gender']  # editable fields can't be display_links

    # `list_filter` allow us to get filter side bar to filter on specific field
    list_filter = ['gender', 'age']

    # `search_fields` provide a search bar at top
    search_fields = ['first_name']

    # we can add `custom fields` to our model list view
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class PassportAdmin(admin.ModelAdmin):
    list_display = ["person", "passport_id",
                    "country", "issue_date", "expire_date"]

    fields = ["person", "passport_id",
              "country", "expire_date"]

    # custom `actions` to perform on bulk data
    actions = [increase_expiry_date, decrease_expiry_date]


# just add custom adminmodel along with model
admin.site.register(Person, PersonAdmin)

admin.site.register(Passport, PassportAdmin)

admin.site.register(Car)
admin.site.register(House)
