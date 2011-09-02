from django.db.models import signals

from publisher.models import Publisher


def publish(sender, instance, action, reverse, model, pk_set, **kwargs):
    if model == Publisher:
        if pk_set and action == 'post_add':
            publishers = Publisher.objects.filter(pk__in=pk_set)
            for publisher in publishers:
                publisher.publish(instance)

signals.m2m_changed.connect(publish)
