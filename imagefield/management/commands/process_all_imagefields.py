from django.core.management.base import BaseCommand

from imagefield.fields import IMAGE_FIELDS


class Command(BaseCommand):
    def handle(self, **options):
        for field in IMAGE_FIELDS:
            self.stdout.write('%s: %s' % (
                field.model._meta.label,
                field.name,
            ))

            queryset = field.model._default_manager.all()
            count = queryset.count()
            for index, instance in enumerate(queryset):
                fieldfile = getattr(instance, field.name)
                if fieldfile and fieldfile.name:
                    for key in field.formats:
                        fieldfile.process(key)

                if index % 10 == 0:
                    progress = '*' * int(index / count * 50)
                    self.stdout.write('\r|%s|' % progress.rjust(50), ending='')
            self.stdout.write('\r|%s|' % ('*' * 50,))