from django import forms
from .models import Devices

#
# class DevicesModelForm(forms.ModelForm):
#     class Meta:
#         model = Devices
#
#     def __init__(self, *args, **kwargs):
#         forms.ModelForm.__init__(self, *args, **kwargs)
#         self.fields['devices'].queryset = Devices.avail_devices.all()
