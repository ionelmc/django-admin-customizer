from django.db import models

def get_type_for(field):
    if isinstance(field, models.ForeignKey):
        return 'fk'
    elif isinstance(field, models.ManyToManyField):
        return 'mtm'
    elif isinstance(field, models.OneToOneField):
        return 'oto'
    else:
        return 'other'

class AvailableFieldManager(models.Manager):
    def get_by_field(self, model, field):
        return self.get(
            name = field.name,
            type = get_type_for(field),
            model = model
        )

    def create_by_field(self, model, field):
        return self.create(
            name = field.name,
            type = get_type_for(field),
            model = model
        )
