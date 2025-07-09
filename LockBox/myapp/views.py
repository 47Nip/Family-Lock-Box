

import random
import string
from django.shortcuts import redirect, render
from myapp.models import UserProfile
from django.contrib import messages  # To show feedback messages
from django.contrib.auth.hashers import make_password #take password as hash
from django.contrib.auth.hashers import check_password #take password from hash to text
from .models import UploadedFile
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from .decorators import session_login_required


def navpage(request):
    return render(request, 'nav.html')


def homepage(request):
    return render(request, 'home.html')


def signuppage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validation checks
        if not username:
            return render(request, 'signin.html', {'error': 'Username is required'})

        if password != confirm_password:
            return render(request, 'signin.html', {'error': 'Passwords do not match'})

        # Case-sensitive username check
        if UserProfile.objects.filter(username__exact=username).exists():
            return render(request, 'signin.html', {'error': 'Username already exists'})

        # Case-insensitive email and phone check
        if UserProfile.objects.filter(Q(email__iexact=email) | Q(phone=phone)).exists():
            return render(request, 'signin.html', {'error': 'Email or phone number already exists'})

        # Save the user with hashed password
        hashed_password = make_password(password)
        user = UserProfile(username=username, email=email, phone=phone, password=hashed_password)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('loginpage')  # Redirect to login after successful signup

    return render(request, 'signin.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = UserProfile.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            request.session['username'] = user.username # Store username in session
            request.session['matched_username'] = user.username
            messages.success(request, "Login successful!")
            
            return redirect('homepage')  
        else:
            messages.error(request, "Invalid username or password!")
            return render(request, 'login.html')

    return render(request, 'login.html')

@session_login_required
@csrf_exempt   
def uploadpage(request):
    # Check if the user is logged in
    username = request.session.get('username')
    if not username:
        messages.error(request, "You must be logged in to upload files.")
        return redirect('loginpage')

    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')  # Fetch file from form
        if uploaded_file:
            # Save file with the username from the session
            file_instance = UploadedFile.objects.create(
                username=username,           # ✅ Store the username
                filename=uploaded_file.name,  # Get the file name
                file=uploaded_file           # Save the file
            )
            messages.success(request, f"File '{file_instance.filename}' uploaded successfully!")
            return redirect('upload_file')  # Redirect to the upload page after success
        else:
            messages.error(request, "No file selected. Please choose a file to upload.")
            return redirect('upload_file')  # Redirect back to the upload page for error
    return render(request, 'upload.html')

@session_login_required
def documentpage(request):
    # Get the username from the session
    username = request.session.get('username')
    
    if not username:
        messages.error(request, "You must be logged in to view your documents.")
        return redirect('loginpage')

    # Fetch only the documents uploaded by the logged-in user
    user_documents = UploadedFile.objects.filter(username=username)

    # Pass the filtered documents to the template
    return render(request, 'documentview.html', {'documents': user_documents})

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
@session_login_required
def rename_document(request, file_id):
    username = request.session.get('username')
    new_name = request.POST.get('new_name', '').strip()
    if not new_name:
        return JsonResponse({'success': False, 'error': 'New name cannot be empty.'})

    try:
        document = UploadedFile.objects.get(id=file_id, username=username)
        document.filename = new_name
        document.save()
        return JsonResponse({'success': True, 'new_name': new_name})
    except UploadedFile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Document not found.'})

@require_POST
@session_login_required
def delete_document(request, file_id):
    username = request.session.get('username')
    try:
        document = UploadedFile.objects.get(id=file_id, username=username)
        document.delete()
        return JsonResponse({'success': True})
    except UploadedFile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Document not found.'})




# Generate a unique 12-character alphanumeric code
def generate_unique_code(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.sample(characters * length, length))

@session_login_required

def profilepage(request):
    username = request.session.get('username')  # Fetch username from session

    

    try:
        user_profile = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile does not exist.")
        return redirect('loginpage')

    # Auto-generate unique code if missing
    if not user_profile.generatecode:
        user_profile.generatecode = generate_unique_code()
        user_profile.save()

    # Handle profile update (POST request)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        birth_date = request.POST.get('birth_date')

        if full_name:
            user_profile.full_name = full_name
        if birth_date:
            user_profile.birth_date = birth_date

        if 'profilepicture' in request.FILES:
            user_profile.profilepicture = request.FILES['profilepicture']

        user_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profilepage')

    return render(request, 'profile.html', {'user_profile': user_profile})


def logout_view(request):
    if 'username' in request.session:  # Ensure session exists before clearing
        request.session.flush()  # Completely clear the session
        request.session.clear_expired()  # Remove expired sessions

    messages.success(request, "Logged out successfully!")
    return redirect('loginpage')  # Redirect to login page
@session_login_required
def groupmember(request):
    if request.method == 'POST':
        code_entered = request.POST.get('code')
        try:
            user_profile = UserProfile.objects.get(generatecode=code_entered)
            # Store matched username in session to show in yourgroups page
            request.session['matched_username'] = user_profile.username
            # Save the match info in UserCodeMatch model
            from myapp.models import UserCodeMatch
            logged_in_username = request.session.get('username')
            if logged_in_username:
                UserCodeMatch.objects.create(
                    logged_in_username=logged_in_username,
                    entered_code=code_entered,
                    matched_username=user_profile.username,
                    matched_user_email=user_profile.email,
                    matched_user_profilepicture=user_profile.profilepicture,
                    matched_user_full_name=user_profile.full_name
                )
            # Add success message
            from django.contrib import messages
            messages.success(request, "Code are found")
            return redirect('yourgroups')
        except UserProfile.DoesNotExist:
            from django.contrib import messages
            messages.error(request, "No any user found")
            return render(request, 'membergroup.html')
    else:
        return render(request, 'membergroup.html')

@session_login_required
def yourgroups(request):
    logged_in_username = request.session.get('username', None)
    matched_users = []
    if logged_in_username:
        from myapp.models import UserCodeMatch
        matched_users = UserCodeMatch.objects.filter(logged_in_username=logged_in_username)
    return render(request, 'yourgroups.html', {'matched_users': matched_users})

from myapp.models import UploadedFile

@session_login_required
def groupdocument(request, matched_username):
    # Get documents uploaded by the matched user
    documents = UploadedFile.objects.filter(username=matched_username)
    return render(request, 'group_document.html', {'documents': documents, 'matched_username': matched_username})
