from django import forms
from converter.models import ReimburseModel, MileageModel

class ReimburseForm(forms.ModelForm):
	class Meta:
		model = ReimburseModel
		fields = ['source']


class MileageForm(forms.ModelForm):
	class Meta:
		model = MileageModel
		fields = ['source']