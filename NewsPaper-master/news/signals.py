# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
#
# from news.models import PostCategory
# from news.utils import send_notifications
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers_users = []
#
#         for cat in categories:
#             subscribers = cat.subscribers.all()
#             subscribers_users += [s for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers_users)
