from django.db import models


class Tenant(models.Model):

    name = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


class DataSource(models.Model):

    SOURCE_TYPES = [

        ('SAP', 'SAP'),

        ('UTILITY', 'Utility'),

        ('TRAVEL', 'Travel'),

    ]

    tenant = models.ForeignKey(

        Tenant,

        on_delete=models.CASCADE,

        null=True,

        blank=True

    )

    source_type = models.CharField(

        max_length=20,

        choices=SOURCE_TYPES

    )

    uploaded_at = models.DateTimeField(

        auto_now_add=True

    )


class RawRecord(models.Model):

    source = models.ForeignKey(

        DataSource,

        on_delete=models.CASCADE

    )

    raw_data = models.JSONField()

    status = models.CharField(

        max_length=30,

        default='PENDING'

    )


class NormalizedRecord(models.Model):

    raw_record = models.OneToOneField(

        RawRecord,

        on_delete=models.CASCADE

    )

    scope = models.CharField(

        max_length=20

    )

    normalized_value = models.FloatField()

    review_status = models.CharField(

        max_length=30,

        default='PENDING'

    )


class AuditLog(models.Model):

    record = models.ForeignKey(

        RawRecord,

        on_delete=models.CASCADE

    )

    action = models.CharField(

        max_length=100

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return (

            f"{self.record.id}"

            +

            "-"

            +

            self.action

        )