# # adapters.py
#
# from allauth.account.adapter import DefaultAccountAdapter
# from django.urls import reverse
# from user.models import EmailVerificationLink
#
#
# class CustomAccountAdapter(DefaultAccountAdapter):
#
#     def send_mail(self, template_prefix, email, context):
#         # This method is called when allauth sends an email (for email verification, password reset, etc.)
#         user = context.get('user')
#
#         if template_prefix == 'account/email/password_reset_key':
#             # Handle password reset link
#             url = self.build_absolute_uri(reverse('account_reset_password_from_key', args=[context['key']]))
#             EmailVerificationLink.objects.create(user=user, purpose='password_reset', link=url)
#
#         elif template_prefix == 'account/email/email_confirmation':
#             # Handle email verification link
#             url = self.build_absolute_uri(reverse('account_confirm_email', args=[context['key']]))
#             EmailVerificationLink.objects.create(user=user, purpose='email_verification', link=url)
#
#         # Optionally print the URL in the console for reference (can be useful during testing)
#         print(f"Generated link: {url}")
