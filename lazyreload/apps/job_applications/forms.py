
class LazyJobApplicationForm(forms.ModelForm):
    class Meta:
        model = LazyJobApplication
        fields = [
            'company_id',
            'profile_id',
            'job_title',
            'job_ad_text',
            'salary_expectation',
            'to_highlight',
            'job_type',
            'cover_letter',
        ]
        widgets = {
            'company_id': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_id': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_ad_text': forms.Textarea(attrs={'class': 'form-control'}),
            'salary_expectation': forms.NumberInput(attrs={'class': 'form-control'}),
            'to_highlight': forms.Textarea(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control'}),
        }