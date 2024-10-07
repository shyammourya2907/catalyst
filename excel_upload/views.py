from django.shortcuts import render
import pandas as pd
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from excel_upload.models import Company, CSVFile
from excel_upload.forms import CSVFileForm, FilterForm
from rest_framework import generics
from .serializers import CompanySerializer
from django.db.models import Q
from celery import shared_task


# to chang the test is done on only 1000 rows
#add authentication to this apis session authentication
# verify the user without sending email
#create a middleware or session authentication for this apis
#create a cron to run to pull data from the table
#collect dat to filter along with dropdown
# pages login,logout, filter, signup, upload, admin
# write logic to upload the file progress bar
#show filter for the progress bar
#set env file and use postgres sql
#create a readme file
#upload to git write test cases


@login_required
def csv_file_list(request):
    csv_files = CSVFile.objects.all()
    return render(request, 'csv_file_list.html', {'csv_files': csv_files})


class CompanyList(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        # breakpoint()
        queryset = Company.objects.all()
        industry = self.request.query_params.get('industry', None)
        year_founded = self.request.query_params.get('year_founded', None)
        city = self.request.query_params.get('city', None)
        state = self.request.query_params.get('state', None)
        country = self.request.query_params.get('country', None)
        keyword = self.request.query_params.get('keyword', None)

        if industry is not None and industry != '':
            queryset = queryset.filter(industry__icontains=industry)

        if year_founded is not None and year_founded != '':
            # Convert the year_founded filter to float for comparison
            try:
                year_founded = float(year_founded)
                queryset = queryset.filter(year_founded=year_founded)
            except ValueError:
                pass  # Handle the case where conversion fails

        if country is not None and country != '':
            queryset = queryset.filter(country=country)

        if state is not None and state != '':
            queryset = queryset.filter(locality__icontains=state)

        if city is not None and city != '':
            queryset = queryset.filter(locality__icontains=city)

        if keyword is not None and keyword != '':
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(domain__icontains=keyword))

        return queryset


# create a cron which should run when the function or time is triggered
# create a filter api
# store data into splitted form country city state
# yearfounded
# industry
# employess from empolyees to
# def store_companies_data(csv_file):
#     data = pd.read_csv(csv_file)
#     for _, row in data.iterrows():
#  pull city state country for this row
#         Company.objects.create(
#             company_id=row['Unnamed: 0'],
#             name=row['name'],
#             domain=row['domain'],
#             year_founded=row.get('year founded'),
#             industry=row['industry'],
#             size_range=row['size range'],
#             locality=row['locality'],
#             country=row['country'],
#             linkedin_url=row['linkedin url'],
#             current_employee_estimate=row.get('current employee estimate'),
#             total_employee_estimate=row.get('total employee estimate'),
#         )

@shared_task
def process_csv(csv_file_path, csv_file_name):
    try:
        print(f"Process started for file path {csv_file_path} and name {csv_file_name}")
        data = pd.read_csv(csv_file_path)

        # for _, row in data.iterrows():
        for _, row in data.iterrows():
            Company.objects.create(
                name=row['name'],
                domain=row['domain'],
                year_founded=row.get('year founded'),
                industry=row['industry'],
                size_range=row['size range'],
                locality=row['locality'],
                country=row['country'],
                linkedin_url=row['linkedin url'],
                current_employee_estimate=row.get('current employee estimate'),
                total_employee_estimate=row.get('total employee estimate'),
            )

        # Mark CSV file processing as complete
        csv_file = CSVFile.objects.get(csv_file=csv_file_name)
        csv_file.database_uploaded_completed = True
        csv_file.save()
        print(f"Process ended for file path {csv_file} and name {csv_file_name}")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# Expected columns and their types
expected_columns = {
    # 'Unnamed: 0': 'int64',
    'name': 'object',
    'domain': 'object',
    'year founded': 'float64',
    'industry': 'object',
    'size range': 'object',
    'locality': 'object',
    'country': 'object',
    'linkedin url': 'object',
    'current employee estimate': 'int64',
    'total employee estimate': 'int64'
}

@login_required()
def upload_file(request):
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        # breakpoint()
        if form.is_valid():
            file = request.FILES['csv_file']
            try:
                # Load CSV file
                data = pd.read_csv(file)
                # Validate columns
                if list(data.columns[1:]) != list(expected_columns.keys()):
                    return JsonResponse({"error": "Invalid columns in the CSV file."}, status=400)

                # Validate data types
                for column, expected_type in expected_columns.items():
                    if data[column].dtype != expected_type:
                        return JsonResponse({"error": f"Column '{column}' has an invalid data type."}, status=400)

                csv_file_instance = CSVFile.objects.create(csv_file=file)
                print(f"{csv_file_instance.csv_file} and name is {csv_file_instance.csv_file.name} object is created")
                process_csv.delay(csv_file_instance.csv_file.path, csv_file_instance.csv_file.name)
                return JsonResponse({"message": "File uploaded successfully."}, status=200)

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"error": "Invalid form."}, status=400)

    return render(request, 'upload.html')


@login_required
def filter_view(request):
    total_results = 0
    if request.method == 'POST':

        form = FilterForm(request.POST or None)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            founded_year = form.cleaned_data['founded_year']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            county = form.cleaned_data['county']
            industry = form.cleaned_data['industry']

            # Construct API URL
            url = "http://127.0.0.1:8000/excel/companies/?"

            params = {
                'keyword': search_text,
                'founded_year': founded_year,
                'state': state,
                'city': city,
                'county': county,
                'industry': industry,
            }
            # Remove empty params
            params = {k: v for k, v in params.items() if v != ''}

            # Make API request

            response = requests.request("GET", url, params=params)
            data = response.json()
            total_results = len(data)  # Adjust based on your API response format
            return render(request, 'filter_data.html', {'form': form, 'total_results': total_results})
        else:
           return JsonResponse({"error": "Invalid form."}, status=400)
    else:
        form = FilterForm()

    return render(request, 'filter_data.html', {'form': form, 'total_results': total_results})





def download_sample(request):
    # Create a DataFrame with dummy data
    sample_data = pd.DataFrame({
        'company id': [1, 2],
        'name': ['Company A', 'Company B'],
        'domain': ['companya.com', 'companyb.com'],
        'year founded': [1990, 2000],
        'industry': ['IT', 'Retail'],
        'size range': ['100-500', '500-1000'],
        'locality': ['New York', 'Los Angeles'],
        'country': ['USA', 'USA'],
        'linkedin url': ['http://linkedin.com/companya', 'http://linkedin.com/companyb'],
        'current employee estimate': [200, 600],
        'total employee estimate': [300, 700]
    })

    # Convert to CSV and return as download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_data.csv"'
    sample_data.to_csv(path_or_buf=response, index=False)
    return response
