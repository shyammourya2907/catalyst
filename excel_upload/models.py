from django.db import models


class Company(models.Model):
    # company_id = models.IntegerField()
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.CharField(max_length=252, null=True, blank=True) #please check the data
    industry = models.CharField(max_length=255)
    size_range = models.CharField(max_length=50)
    locality = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    linkedin_url = models.URLField(max_length=500, null=True, blank=True)
    current_employee_estimate = models.IntegerField(null=True, blank=True)
    total_employee_estimate = models.IntegerField(null=True, blank=True)
    # city = models.CharField(max_length=255, null=True, blank=True)
    # state = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class CSVFile(models.Model):
    csv_file = models.FileField(upload_to='csv/')  # Use relative path
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    database_uploaded_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.csv_file.name} uploaded on {self.created_at}"


