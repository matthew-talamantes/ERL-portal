from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.db import transaction

from datetime import date, timedelta

from useraccount.models import ErlUser

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
                while shiftDate <= endRepeat:
                    shift = ShiftInstance(baseShift=instance, date=shiftDate, startTime=instance.startTime, endTime=instance.endTime, name=instance.name, description=instance.description, staffSlots=instance.staffSlots, volSlots=instance.volSlots, minSlots=instance.minSlots, slots=instance.slots)
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
        
        else:
            shift = ShiftInstance.objects.create(baseShift=instance, date=instance.date, startTime=instance.startTime, endTime=instance.endTime, name=instance.name, description=instance.description, staffSlots=instance.staffSlots, volSlots=instance.volSlots, minSlots=instance.minSlots, slots=instance.slots)
            shift.save()

@receiver(m2m_changed, sender=BaseShift.defaultStaff.through)
def default_staff_changed(sender, instance, **kwargs):
    staffList = [x for x in kwargs['pk_set']]
    shifts = [x for x in ShiftInstance.objects.filter(baseShift=instance)]
    shiftStaffRelation = ShiftInstance.staff.through

    relations = []
    for shift in shifts:
        relations.extend([shiftStaffRelation(erluser_id=staff, shiftinstance_id=shift.uid) for staff in staffList])
        shift.save()
    
    shiftStaffRelation.objects.bulk_create(relations, batch_size=100, ignore_conflicts=True)

@receiver(m2m_changed, sender=BaseShift.defaultVols.through)
def default_vols_changed(sender, instance, **kwargs):
    volsList = [x for x in kwargs['pk_set']]
    shifts = [x for x in ShiftInstance.objects.filter(baseShift=instance)]
    shiftVolsRelation = ShiftInstance.vols.through

    relations = []
    for shift in shifts:
        relations.extend([shiftVolsRelation(erluser_id=vol, shiftinstance_id=shift.uid) for vol in volsList])
        shift.save()

    shiftVolsRelation.objects.bulk_create(relations, batch_size=100, ignore_conflicts=True)
