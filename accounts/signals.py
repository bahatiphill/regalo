from accounts.models import Churches
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from wallet.models import Ikofi


@receiver(post_save, sender=Churches)
def finalize_account(sender, instance, **kwargs):
    #add church to church  Group and create its ikofi instance
    print("######### Dispatcher being called")    
    if kwargs.get('created', False):
        
        #add to group
        g = Group.objects.get(name='churches')
        #g.user_set.add(instance)
        instance.groups.add(g)

        #create its IKOFI
        new_ikofi = Ikofi(church=instance, amount=0)
        new_ikofi.save()
        print("######### Dispatcher finnish") 

