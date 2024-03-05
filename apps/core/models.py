from django.db import models

# Create your models here.
# class AiSettings(models.Model): # not used in CoverLetterGenerator
#     ai_setting_name = models.CharField(max_length=60, blank=False, default="new")
#     other_profile_id = models.ForeignKey("users.LazyUserProfile", on_delete=models.CASCADE)
#     # enable user to save a setting as favorite to reuse it
#     favorite = models.BooleanField(default=False,
#                                    verbose_name="Saved as Favorite")
#     # GPT temperature deterministic vs. creative
#     temperature = models.FloatField(default=0.5, verbose_name="Rational/Creative")
#     word_count = models.IntegerField(default=320, verbose_name="How long should the letter be")
#     # GPT 3.5 or 4 - high is default, for futur cost tiering
#     QUALITY_CHOICES = {
#         "low": "Low",
#         "high": "High",
#     }
#     quality = models.CharField(choices=QUALITY_CHOICES, default="high", max_length=20, blank=True)
