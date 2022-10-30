from django.core.management.base import BaseCommand, CommandError

from travelblog.scraper import main

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
            try:
                main()
                print('Hello, Python')

            except Exception as error:
                raise CommandError('Poll "%s" does not exist %s' % error)


            self.stdout.write(self.style.SUCCESS('Successfully parsed'))