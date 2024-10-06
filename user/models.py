# # models.py
#
# from django.db import models
# from django.contrib.auth.models import User
#
#
# class EmailVerificationLink(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     purpose = models.CharField(max_length=50)  # E.g., "email_verification" or "password_reset"
#     link = models.URLField()  # Store the generated link
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.purpose}"
