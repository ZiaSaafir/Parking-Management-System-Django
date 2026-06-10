# from django.db import models

# # Create your models here.
# class UserProfile(models.Model):

#     ROLE_CHOICES = [
#         ("ADMIN", "Admin"),
#         ("OPERATOR", "Operator"),
#         ("MANAGER", "Manager"),
#     ]

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE
#     )

#     role = models.CharField(
#         max_length=20,
#         choices=ROLE_CHOICES
#     )