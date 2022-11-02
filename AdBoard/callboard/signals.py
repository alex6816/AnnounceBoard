from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Announcement)
def notify_new_ann(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            if str(Announcement.author) != str(user.username):
                title = f'Новое объявление!'
                msg = f'Здравствуйте, {user.username}! На нашем сайте опубликовано новое объявление!'
                email = settings.DEFAULT_FROM_EMAIL
                ad_email = user.email

                send_mail(subject=title, message=msg, from_email=email, recipient_list=[ad_email, ])


@receiver(post_save, sender=Respond)
def notify_new_respond(sender, instance, created, **kwargs):
    user = User.objects.get(pk=instance.respond_user_id)   #  автор отклика

    if created:
        pk_ann = instance.respond_ann_id
        user = f'{user.username}'
        user_id = Announcement.objects.get(pk=pk_ann).author_id
        ann_title = Announcement.objects.get(pk=pk_ann).title

        title = f'Новый отклик на Ваше объявление!'
        msg = f'На Ваше объявление "{ann_title}" пришел новый отклик от пользователя {user}. \n' \
              f'Для просмотра перейдите в раздел "Мои объявления"'
        email = settings.DEFAULT_FROM_EMAIL
        ann_email = User.objects.get(pk=user_id).email

        send_mail(subject=title, message=msg, from_email=email, recipient_list=[ann_email, ])


@receiver(post_save, sender=Respond)
def notify_status(sender, instance, created, **kwargs):
    user = User.objects.get(pk=instance.respond_user_id)  # автор отклика

    if not (created) and instance.status == True:
        pk_ann = instance.respond_ann_id
        ann_title = Announcement.objects.get(pk=pk_ann).title

        title = f'Ваш отклик принят!'
        msg = f'Здравствуйте, {user.username}! Ваш отклик на объявление "{ann_title}" принят.'
        email = settings.DEFAULT_FROM_EMAIL
        res_email = user.email

        send_mail(subject=title, message=msg, from_email=email, recipient_list=[res_email, ])