from django.core.management.base import BaseCommand, CommandError
from abTest.models import TestResult, StatisticRow

class Command(BaseCommand):
    args = ''
    help = 'aggregate ab stats'

    def handle(self, *args, **options):
        rows = TestResult.objects.all()
        statistic = StatisticRow.createStatistic(rows, True)
        print statistic
