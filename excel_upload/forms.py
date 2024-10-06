# import form class from django
from django import forms
from excel_upload.constants import country_choices, industry_choices, state_choices, city_choices

# import GeeksModel from models.py
from excel_upload.models import CSVFile


class CSVFileForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['csv_file']

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file and not csv_file.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV files are allowed.")
        return csv_file


class FilterForm(forms.Form):
    search_text = forms.CharField(max_length=100, required=False, label='Search')
    founded_year = forms.ChoiceField(choices=[('', 'Select Year')] + [(str(year), str(year)) for year in range(1800, 2025)], required=False)
    state = forms.ChoiceField(choices=state_choices, required=False)
    city = forms.ChoiceField(choices=city_choices, required=False)
    county = forms.ChoiceField(choices=country_choices, required=False)
    industry = forms.ChoiceField(choices=industry_choices, required=False)
