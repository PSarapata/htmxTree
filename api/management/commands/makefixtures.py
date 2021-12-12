from django.core.management.base import BaseCommand
from api.models import Tree, SimpleElement
from django.conf import settings
import random
import json

class Command(BaseCommand):
    help = 'Initiate db with fixtures for testing'

    def handle(self, *args, **options):
        # Create 1000 simple elements if none exist
        if SimpleElement.objects.count() == 0:
            for i in range(1000):
                SimpleElement.objects.create(name='Simple Element #{}'.format(i))
            # Create 25 top level trees
            for i in range(25):
                r = random.choice(SimpleElement.objects.all())
                Tree.objects.create(parent_row=None, row=r)
        # Randomly link simple elements to trees
        if Tree.objects.count() != 25:
            for el in random.sample(list(SimpleElement.objects.all()), 500):
                random_parent = random.choice(SimpleElement.objects.all())
                if random_parent == el:
                    continue
                Tree.objects.create(row=el, parent_row=random_parent, lp=Tree.objects.filter(row=el, parent_row=random_parent).count() + 1)
        
        with open(f"{settings.BASE_DIR}" + '/api/fixtures/tree.json', 'w') as f:
            feed = "[\n" + ",\n".join([json.dumps(tree.to_json(), indent=4) for tree in Tree.objects.all()]) + "\n]"
            f.write(feed)
            f.close()

        print("DB has {} trees".format(Tree.objects.count()))