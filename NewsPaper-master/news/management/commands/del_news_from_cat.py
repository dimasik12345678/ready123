from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = "Удаляет все новости в выбранной категории, указать категорию после команды"

    def add_arguments(self, parser):
        parser.add_argument("category", type=str)

    def handle(self, *args, **options):
        answer = input(
            f"Вы действительно хотите удалить все статьи в категории {options['category']}?\n"
            "Напишите 'Y' или 'yes' чтобы удалить:\n"
        )

        if answer != "yes".lower or "Y".lower:
            self.stdout.write(self.style.ERROR("Отменено"))
            return
        try:
            category = Category.objects.get(name=options["category"])
            Post.objects.filter(category=category).delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Succesfully deleted all news from category {category.name}"
                )
            )  # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Could not find category {category.name}")
            )
