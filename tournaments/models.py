from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Creating roles and assigning them programmatically
def create_roles():
    va_group, created = Group.objects.get_or_create(name="VA")
    
    # Add custom permissions
    has_va_permission = Permission.objects.create(codename='has_va_permission', name='has_va_permission')

    # Assign permissions to groups
    va_group.permissions.add(has_va_permission)
    


class Tournament(models.Model):
    event_name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    age_group = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=[('boys', 'Boys'), ('girls', 'Girls'), ('both', 'Both')])
    event_type = models.CharField(max_length=50, choices=[('dual', 'Dual'), ('individual', 'Individual'), ('both', 'Both')])
    style = models.CharField(max_length=50, choices=[('folkstyle', 'Folkstyle'), ('freestyle', 'Freestyle'), ('both', 'Both')])
    flyer_url = models.URLField(blank=True, null=True)
    club_name = models.CharField(max_length=255)
    tournament_director = models.CharField(max_length=255)
    contact_info = models.TextField()
    
    def __str__(self):
        return self.event_name


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=10)
    preferred_age_group = models.CharField(max_length=50)
    preferred_gender = models.CharField(max_length=20, choices=[('boys', 'Boys'), ('girls', 'Girls'), ('both', 'Both')])
    preferred_style = models.CharField(max_length=50, choices=[('folkstyle', 'Folkstyle'), ('freestyle', 'Freestyle'), ('both', 'Both')])

    def __str__(self):
        return self.user.username



class TournamentDirector(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()

    def __str__(self):
        return self.name



class VirtualAssistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    



class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    link_url = models.URLField(max_length=200,help_text="Enter the URL for the banner link")
    
    
    def __str__(self):
        return f"Banner {self.id}"