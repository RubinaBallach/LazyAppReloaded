from django.contrib import admin
from .models import Company, LazyJobApplication

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ['company_id', 'company_name',
              'company_website', 'company_location',
              'company_mail', 'company_info']
    readonly_fields = ['company_id']

@admin.register(LazyJobApplication)
class LazyJobApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ['lazy_application_id', 'profile_id', 'company_id', 'ad_link']
    fields = ['lazy_application_id', 'profile_id', 'company_id','ad_link', 'job_title', 'job_ad_text',
              'recruiter_name', 'recruiter_mail', 'recruiter_phone',
              'job_type', 'salary_expectation', 'to_highlight', 'cover_letter', 'status']

