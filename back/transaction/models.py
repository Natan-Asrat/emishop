from django.db import models
from django.utils.timesince import timesince
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('reported', 'Reported')
    ]

    buyer = models.ForeignKey('account.User', related_name='reservations', on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', related_name='reservations', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    coins_spent = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller_accepted = models.BooleanField(default=False)
    report_reason = models.TextField(blank=True, null=True)
    reported_at = models.DateTimeField(null=True, blank=True)
    cancelled_by = models.ForeignKey('account.User', related_name='cancelled_reservations', 
                                   on_delete=models.SET_NULL, null=True, blank=True)

    def reported_at_formatted(self):
        return timesince(self.reported_at) if self.reported_at else None
    class Meta:
        ordering = ['-created_at']