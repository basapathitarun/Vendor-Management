import time

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.db.models import Count, Avg


class vendor(models.Model):
    """Vendor Model"""
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True,max_length=50)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class purchaseOrder(models.Model):

    """Purchase Order (PO) Model"""
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('completed','Completed'),
        ('canceled','Canceles')
    ]
    po_number = models.CharField(unique=True,max_length=20)
    vendor = models.ForeignKey(vendor,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    delivery_date = models.DateTimeField()
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.po_number


class Performance(models.Model):

    """Historical Performance Model"""
    vendor = models.ForeignKey(vendor,on_delete=models.CASCADE)
    data = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.data}"


@receiver(post_save, sender=purchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):

    """This function automatcially invoke when purchaseOrder model invokes"""

    if instance.status == 'completed' and instance.delivery_date is None:
        """ checks if status completes with delivery date is None, Updates delivery date with current timings"""
        instance.delivery_date = timezone.now()
        instance.save()

    """Update On-Time Delivery Rate"""
    completed_orders = purchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
    on_time_deliveries = completed_orders.filter(delivery_date__lte=F('delivery_date'))
    on_time_delivery_rate = on_time_deliveries.count() / completed_orders.count()
    instance.vendor.on_time_delivery_rate = on_time_delivery_rate if on_time_delivery_rate else 0

    """Update Quality Rating Average"""
    completed_orders_with_rating = completed_orders.exclude(quality_rating__isnull=True)
    quality_rating_avg = completed_orders_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    instance.vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg else 0

    """Update Average Response Time"""
    response_times = purchaseOrder.objects.filter(vendor=instance.vendor).values_list('acknowledgement_date', 'issue_date')
    average_response_time = sum((ack_date - issue_date).total_seconds() for ack_date, issue_date in response_times) / len(response_times) if response_times else 0
    instance.vendor.average_response_time = max(average_response_time, 0)

    """Update Fulfillment Rate"""
    fulfilled_orders = purchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
    fulfillment_rate = fulfilled_orders.count() / purchaseOrder.objects.filter(vendor=instance.vendor).count()
    instance.vendor.fulfillment_rate = fulfillment_rate

    """Save the updated vendor instance"""
    instance.vendor.save()

    """Create or update Performance instance"""
    Performance.objects.update_or_create(
        vendor=instance.vendor,
        defaults={
            'data':timezone.now(),
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate
        }
    )
