from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Tournament, ParentProfile
from django.contrib.auth.forms import UserCreationForm
from .forms import TournamentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

from .models import VirtualAssistant
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tournament, Banner
from django.contrib.auth.decorators import login_required, permission_required



def has_permission_or_is_superuser(user):
    return user.has_perm('has_va_permission') or user.is_superuser



def home_view(request):
    # Fetch all tournaments
    tournaments = Tournament.objects.all()
    search_query = request.GET.get('search', '')

    # Filter by user preferences if authenticated
    if request.user.is_authenticated:
        try:
            parent_profile = ParentProfile.objects.get(user=request.user)
            tournaments = tournaments.filter(
                age_group=parent_profile.preferred_age_group,
                gender=parent_profile.preferred_gender,
                style=parent_profile.preferred_style
            )
        except ParentProfile.DoesNotExist:
            # If no parent profile exists, show all tournaments without filtering
            pass

    # Apply search filter if a search query is provided
    if search_query:
        tournaments = tournaments.filter(
            Q(event_name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(date__icontains=search_query)
        )

    # Pagination: Display 6 tournaments per page
    paginator = Paginator(tournaments, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    banners = Banner.objects.all()

    return render(request, 'user_pages/home_page.html', {
        'tournaments': page_obj,
        'search_query': search_query,
        'banners':banners
    })





@user_passes_test(has_permission_or_is_superuser, login_url='/login/')
def tournament_list(request):
    tournaments = Tournament.objects.all()
    if request.user.is_authenticated:
        try:
            parent_profile = ParentProfile.objects.get(user=request.user)
            tournaments = tournaments.filter(
                age_group=parent_profile.preferred_age_group,
                gender=parent_profile.preferred_gender,
                style=parent_profile.preferred_style
            )
        except ParentProfile.DoesNotExist:
            pass
    return render(request, 'tournaments/tournament_list.html', {'tournaments': tournaments})




def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            try:
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('login')
            except:
                messages.error(request, "An error occurred during registration.")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'registration/register.html')

# Login View using Bootstrap form
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')  # Redirect to tournament list
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('login')
    return render(request, 'registration/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logging out



def tournament_details(request, tournament_id):
    # Fetch the tournament by ID or return a 404 error if not found
    tournament = get_object_or_404(Tournament, id=tournament_id)
    
    return render(request, 'user_pages/tournament_details.html', {
        'tournament': tournament
    })



@user_passes_test(has_permission_or_is_superuser, login_url='/login/')
def add_tournament(request):
    if request.method == 'POST':
        # Extracting data from the POST request
        event_name = request.POST.get('event_name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        age_group = request.POST.get('age_group')
        gender = request.POST.get('gender')
        event_type = request.POST.get('event_type')
        style = request.POST.get('style')
        flyer_url = request.POST.get('flyer_url', '')
        club_name = request.POST.get('club_name')
        tournament_director = request.POST.get('tournament_director')
        contact_info = request.POST.get('contact_info')

        # Validation (optional)
        if not event_name or not date or not location:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'tournaments/add_tournament.html', {'form_data': request.POST})

        # Save to the database
        Tournament.objects.create(
            event_name=event_name,
            date=date,
            location=location,
            age_group=age_group,
            gender=gender,
            event_type=event_type,
            style=style,
            flyer_url=flyer_url,
            club_name=club_name,
            tournament_director=tournament_director,
            contact_info=contact_info
        )
        messages.success(request, "Tournament added successfully.")
        return redirect('dashboard')

    # Render the empty form
    return render(request, 'tournaments/add_tournament.html')



@user_passes_test(has_permission_or_is_superuser, login_url='/login/')
def update_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            messages.success(request, "Tournament updated successfully.")
            return redirect('tournament_list')
    else:
        form = TournamentForm(instance=tournament)
    return render(request, 'tournaments/update_tournament.html', {'form': form})
@user_passes_test(has_permission_or_is_superuser, login_url='/login/')
def delete_tournament(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    if request.method == 'POST':
        tournament.delete()
        messages.success(request, "Tournament deleted successfully.")
        return redirect('dashboard')
    return render(request, 'tournaments/delete_tournament.html', {'tournament': tournament})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ParentProfile.objects.create(
                user=user,
                postal_code='',  # Default value
                preferred_age_group='both',  # Default value
                preferred_gender='both',  # Default value
                preferred_style='both'  # Default value
            )
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




@user_passes_test(lambda u: u.is_superuser)
def add_virtual_assistant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        is_active = request.POST.get('is_active') == 'True'  # Convert to boolean
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already in use.")
            return redirect('add_virtual_assistant')

        # Create a new user for the Virtual Assistant
        user = User.objects.create_user(username=name, email=email, password='123')
        
        # Create the Virtual Assistant and link it to the user
        assistant = VirtualAssistant(user=user, name=name, email=email, is_active=is_active)
        assistant.save()

        messages.success(request, 'Virtual Assistant added successfully!')
        return redirect('virtual_assistant_list')

    return render(request, 'virtual_assistants/add_assistant.html')
@user_passes_test(lambda u: u.is_superuser)
def virtual_assistant_list(request):
    assistants = VirtualAssistant.objects.all()
    return render(request, 'virtual_assistants/assistant_list.html', {'assistants': assistants})
@user_passes_test(lambda u: u.is_superuser)
def edit_virtual_assistant(request, pk):
    assistant = get_object_or_404(VirtualAssistant, pk=pk)

    if request.method == 'POST':
        assistant.name = request.POST.get('name')
        assistant.email = request.POST.get('email')
        assistant.is_active = request.POST.get('is_active') == 'True'

        # Update User if email has changed
        user = assistant.user
        user.email = assistant.email
        user.save()

        assistant.save()

        messages.success(request, 'Virtual Assistant updated successfully!')
        return redirect('virtual_assistant_list')

    return render(request, 'virtual_assistants/edit_assistant.html', {'assistant': assistant})

@user_passes_test(lambda u: u.is_superuser)
def delete_virtual_assistant(request, pk):
    assistant = get_object_or_404(VirtualAssistant, pk=pk)
    assistant.user.delete()  # Delete the associated user
    assistant.delete()  # Delete the assistant

    messages.success(request, 'Virtual Assistant deleted successfully!')
    return redirect('virtual_assistant_list')




def view_banners(request):
    banners = Banner.objects.all()
    return render(request, 'banners/view_banners.html', {'banners': banners})


def add_banners(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        link_url = request.POST.get('link_url')

        if image and link_url:
            banner = Banner(image=image, link_url=link_url)
            banner.save()
            return redirect('banner_list')  # Redirect to success page after saving

    return render(request, 'banners/add_banner.html')
def delete_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    banner.delete()
    return redirect('banner_list')
