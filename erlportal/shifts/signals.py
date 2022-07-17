from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction

from datetime import date, timedelta

from .models import BaseShift, ShiftInstance

@receiver(post_save, sender=BaseShift)
def create_instance_shifts(sender, instance, created, **kwargs):
    if created:
        if instance.repeat:
            transaction.set_autocommit(False)
            
            try:
                if instance.endRepeat:
                    endRepeat = instance.endRepeat
                else:
                    endRepeat = date(instance.date.year + 100, instance.date.month, instance.date.day)
                    
                shiftList = []
                shiftDate = instance.date
                while shiftDate < endRepeat:
                    shift = ShiftInstance(baseShift=instance, date=shiftDate, startTime=instance.starTime, endTime=instance.endTime, name=instance.name, description=instance.description, staffSlots=instance.staffSlots, volSlots=instance.volSlots, minSlots=instance.minSlots, slots=instance.slots)
                    shift.staff.add(instance.defaultStaff.all())
                    shift.vols.add(instance.defaultVols.all())
                    shiftList.append(shift)
                    if instance.repeat == 'everyday':
                        shiftDate += timedelta(days=1)
                    else:
                        shiftDate += timedelta(weeks=1)
                ShiftInstance.objects.bulk_create(shiftList)
            except:
                transaction.rollback()
                raise
            else:
                transaction.commit()
            finally:
                transaction.set_autocommit(True)
