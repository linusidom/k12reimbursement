import os
import pandas as pd

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DeleteView

import time

from expenses import settings
from converter.models import ReimburseModel, MileageModel
from converter.forms import ReimburseForm, MileageForm

from .reimburse import rb_fill_rows, rb_get_category
from .mileage import mg_fill_rows, mg_get_accounts

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# Create your views here.
class ReimburseView(ListView):
	model = ReimburseModel
	template_name = 'converter/reimburse.html'


class MileageView(ListView):
	model = MileageModel
	template_name = 'converter/mileage.html'


class ReimburseErrorView(TemplateView):
	template_name = 'converter/reimburse_error.html'

class MileageErrorView(TemplateView):
	template_name = 'converter/mileage_error.html'

def reimburse_create(request):
	if request.method == 'POST':
		form = ReimburseForm(request.POST, request.FILES)
		if form.is_valid():
			file_upload = form.save(commit=False)
			file_upload.source = request.FILES['source']

			file_upload.save()

			# Load the Data
			df_location = 0
			reimbursement_data = pd.DataFrame(columns=['Date Received','Date Processed','Date Disbursed','Method','Employee Name','First Name','Last Name','Team','Business Purpose','Amount','Processed?','Region','Account Code','Trinet Codes','Tax Year Incurred','Notes'])


			df = pd.read_csv(file_upload.source)
		
			try:
				for i in range(len(df)):
					purposes = rb_get_category(df, i)
					for key, value in purposes.items():
						rb_fill_rows(reimbursement_data, len(reimbursement_data), df_location, key, value)
						df_location += 1
			except:
				return redirect('converter:reimburse_error')

			dest_file_name = 'Converted Reimbursement.csv'
			reimbursement_data.to_csv('./media/uploads/' + dest_file_name, sep=',')
			file_upload.destination = './uploads/' + dest_file_name
			file_upload.save()
			return redirect('converter:reimburse')

	else:
		form = ReimburseForm()
	return render(request, 'converter/file_form.html', {'form':form})




def mileage_create(request):
	if request.method == 'POST':
		form = MileageForm(request.POST, request.FILES)
		if form.is_valid():
			file_upload = form.save(commit=False)
			file_upload.source = request.FILES['source']

			file_upload.save()
			# Load the Data
			df_location = 0
			mileage_data = pd.DataFrame(columns=['Date Received','Date Processed','Date Disbursed','Method','Employee Name','First Name','Last Name','Team','Business Purpose','Amount','Processed?','Region','Account Code','Trinet Codes','Tax Year Incurred','Notes'])


			df = pd.read_csv(file_upload.source)

			try:
				for i in range(len(df)):
					purposes = mg_get_accounts(df, i)
					for key, value in purposes.items():
						mg_fill_rows(mileage_data, len(mileage_data), df_location, key, value)
						df_location += 1
			except:
				return redirect('converter:mileage_error')
			
			dest_file_name = 'Converted Mileage' + time.strftime("%Y%m%d-%H%M%S") + '.csv'
			mileage_data.to_csv('./media/uploads/' + dest_file_name, sep=',')
			file_upload.destination = './uploads/' + dest_file_name
			file_upload.save()
			return redirect('converter:mileage')

	else:
		form = MileageForm()
	return render(request, 'converter/file_form.html', {'form':form})

class ReimburseDeleteView(DeleteView):
	model = ReimburseModel
	success_url = reverse_lazy('converter:reimburse')

	def form_valid(self, form):
		success_url = self.get_success_url()
		os.remove(os.path.join(settings.MEDIA_ROOT, str(self.object.source)))
		os.remove(os.path.join(settings.MEDIA_ROOT, str(self.object.destination)))
		self.object.delete()
		return HttpResponseRedirect(success_url)

class MileageDeleteView(DeleteView):
	model = MileageModel
	success_url = reverse_lazy('converter:mileage')

	def form_valid(self, form):
		success_url = self.get_success_url()
		os.remove(os.path.join(settings.MEDIA_ROOT, str(self.object.source)))
		os.remove(os.path.join(settings.MEDIA_ROOT, str(self.object.destination)))
		self.object.delete()
		return HttpResponseRedirect(success_url)
