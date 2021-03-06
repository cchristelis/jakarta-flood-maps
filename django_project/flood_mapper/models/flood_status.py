    # coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'timlinux'
__project_name = 'jakarta-flood-maps'
__filename = 'village.py'
__date__ = '11/11/14'
__copyright__ = 'tim@kartoza.com'
__doc__ = ''

from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from flood_mapper.models.rt import RT
from django.contrib.auth.models import User

from rest_framework import serializers


class FloodStatus(models.Model):
    """Flood status model."""

    class Meta:
        """Meta class."""
        app_label = 'flood_mapper'

    name = models.CharField(max_length=200)
    rt = models.ForeignKey(
        RT,
        help_text='RT yang terdampak.',
    )
    depth = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text=(
            'Kedalaman dalam meter banjir RT tersebut. <br>'
            'Pilih kedalaman antara 0m and 10m'
        ),
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    date_time = models.DateTimeField(
        verbose_name=u'Date Time (Asia/Jakarta)',
        help_text=(
            'Kapan kedalaman banjir tercapai. <br>'
            'Pergunakan pemilih tanggal dan waktu atau tambahkan sendiri <br>'
            'YYYY-MM-DD hh:mm'
        ))
    recorded_by = models.ForeignKey(User)
    reporter_name = models.CharField(
        max_length=100
    )
    reporting_medium = models.CharField(
        max_length=100
    )
    notes = models.TextField(
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.name

    def save_base(self, *args, **kwargs):
        self.name = '%s -- %s: %s' % (self.date_time, self.rt, self.depth)
        super(FloodStatus, self).save_base(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Overloaded save method."""
        super(FloodStatus, self).save(*args, **kwargs)


class FloodStatusSerializer(serializers.ModelSerializer):

    rw = serializers.SerializerMethodField('get_rw')
    village = serializers.SerializerMethodField('get_village')

    def get_rw(self, obj):
        return obj.rt.rw.id

    def get_village(self, obj):
        return obj.rt.rw.village.id

    class Meta:
        model = FloodStatus
        fields = ('id', 'date_time', 'rt', 'rw', 'village', 'depth')


class FloodStatusFullSerializer(FloodStatusSerializer):

    contact_person = serializers.SerializerMethodField('get_contact_person')
    contact_phone = serializers.SerializerMethodField('get_contact_phone')

    def get_contact_person(self, obj):
        return obj.rt.contact_person

    def get_contact_phone(self, obj):
        return obj.rt.contact_phone

    class Meta:
        model = FloodStatus
        fields = (
            'id', 'date_time', 'rt', 'rw', 'village', 'depth',
            'contact_person', 'contact_phone'
        )
