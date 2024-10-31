from django.shortcuts import render,redirect

from django.views.decorators.http import require_POST

from django.http import JsonResponse

from .models import UserProfile, leaderboard

from image_generator.generator import generate_and_get_digits

import random

from django.db.models import F, FloatField

from django.db.models.functions import Cast

import time
import json


height = 600
width = 800

from django.middleware.csrf import get_token

def get_csrf_token(request):
    # Get the CSRF token for the current session
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

url="http://mysterydigits.vjec.in/"

def load_data_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


@require_POST
def edit_user_profile(request):
    uid = request.POST.get('uid')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    chances_left = request.POST.get('chances_left')

    try:
        user_profile, created = UserProfile.objects.update_or_create(
            uid=uid,
            defaults={
                'name': name,
                'phone': phone,
                'chances_left': chances_left,
            }
        )

        if created:
            return JsonResponse({"message": "New user created successfully."}, status=201)
        else:
            return JsonResponse({"message": "User profile updated successfully."}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def admin_panel_page(request):
    if request.session.get("admin"):
        return render(request,"adminpanel.html")

def admin_login_page(request):
    return render(request, 'adminlogin.html')

def admin_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if username=="ashish" and password=="mysteryashish":
                request.session["admin"]=username

                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"message": "Invalid username or password"}, status=401)

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)



# Function to check changes and update session

def check_changes(request):

    # Check the current state of changesL (you can define how you get this state)



    # Simulate checking for changes

    if request.session.get("changesL")==1:  # Replace with actual condition

        val=  1  # Changes detected

    else:

        val=0

    request.session["changesL"] = 0  # No changes detected



    return JsonResponse({"data":val}, status=200)



def resume_time(request):

    if request.method == 'GET':

        request.session["time"] = time.time()

        response_data = {

            'done': 1,

        }

        return JsonResponse(response_data)

    else:

        return JsonResponse({'error': 'Invalid request method'}, status=400)



def get_leaderboard(request):

    leaderboard_entries = leaderboard.objects.all().order_by('rank')



    leaderboard_data = []

    for entry in leaderboard_entries:

        leaderboard_data.append([

            entry.rank,

            entry.name,

            entry.level,

            entry.avg_time.split(".")[0] + " min",

            entry.eliminated

        ])



    return JsonResponse(leaderboard_data, safe=False)



def update_leaderboard(request):
    # Get the current leaderboard entries
    current_leaderboard = leaderboard.objects.all().order_by('rank')

    # Annotate UserProfile data
    users = UserProfile.objects.annotate(
        lvl_int=Cast('lvl', output_field=FloatField()),
        time_float=Cast('time', output_field=FloatField()),
        chances_int=Cast('chances_left', output_field=FloatField())
    ).order_by('-lvl_int', 'time_float')

    # Create a new leaderboard to compare, limiting to top 10
    new_leaderboard = []

    for rank, user in enumerate(users[:10], start=1):  # Get only the top 10 users
        eliminated = '1' if float(user.chances_int) <= 0 else '0'

        new_leaderboard.append({
            'rank': str(rank),
            'name': user.name,
            'level': user.lvl,
            'avg_time': user.time,
            'eliminated': eliminated
        })

    request.session["changesL"] = 1

    # Check if the leaderboard needs to be updated
    if list(current_leaderboard.values()) != new_leaderboard:
        # Clear the previous leaderboard entries
        leaderboard.objects.all().delete()

        # Create new leaderboard entries
        for entry in new_leaderboard:
            leaderboard.objects.create(**entry)

        # Set changesL to 1 after updating the leaderboard
        return f"Leaderboard updated with {len(new_leaderboard)} entries."

    # No changes made, set changesL to 0
    request.session["changesL"] = 0
    return "No changes to the leaderboard."

def game(request):

    value = request.POST.get('val')
    print(value)

    phone = request.session.get("phone")



    try:

        user_profile = UserProfile.objects.get(phone=phone)

        digits = request.session.get("generated")
        tech=[]
        for i in digits:
            tech.append(i)

        digits=tech
        final = []
        print(digits)
        guessed_digits = []
        for i in value:
            guessed_digits.append(i)
        print(guessed_digits)


        if len(digits)!=len(guessed_digits):
            user_profile.chances_left =int(user_profile.chances_left)-1

            user_profile.save()

            update_leaderboard(request)


            if user_profile.chances_left == 0:

                context = {"continue": "false", "tries": user_profile.chances_left}

                request.session.flush()
                request.session["done"]=1
            else:
                context = {

                            'continue': "true",
                            "tries": user_profile.chances_left,

                            'level': user_profile.lvl,

                            'tries': user_profile.chances_left,


                }
            return JsonResponse(context, status=400)


        else:
            # Initialize the final list to store correct guesses
            final = []

            # Iterate through a copy of the guessed digits
            for guess in guessed_digits[:]:  # Use a copy to avoid modifying the list during iteration
                if guess in digits:
                    digits.remove(guess)          # Remove the digit from the digits list
                    guessed_digits.remove(guess)  # Remove the guess from the guessed digits list
                    final.append(guess)           # Append the correct guess to the final list
                    print("Remaining digits:", digits)
                    print("Remaining guessed digits:", guessed_digits)
                    print("Correct guesses:", final)
                else:
                    print(f"Not a correct guess: {guess}")  # Improved error message

            # Check if the number of correct guesses matches the level
            if len(final) == int(user_profile.lvl):
                print("Level complete!")  # Indicate that the level is complete
        # Add additional logic here for completing the level

                # Proceed with the level-up logic here
                print("Level up!")

                print("true")
                digits=[]
                final=[]

                user_profile.lvl=int(user_profile.lvl)+1

                user_profile.save()

                update_leaderboard(request)

                digits_in_image = load_data_from_json("main/data.json")
                sanam=digits_in_image["level_"+str(user_profile.lvl)]
                r=random.randint(0,19)
                random_entry=sanam[r]
                filename = random_entry['filename']
                guessed_numbers = random_entry['guessed_numbers']
                print(guessed_numbers)
                string=""
                for i in guessed_numbers:
                    string+=i

                request.session["generated"] = string

                request.session["filename"]=filename



                context = {

                    'continue': "true",

                    'level': user_profile.lvl,

                    'tries': user_profile.chances_left,

                    'filepath': "http://mysterydigits.vjec.in/" + request.session["filename"],

                }

                my_time = request.session.get("time")

                avg_time = time.time() - my_time

                avg_time = avg_time / 60

                user_profile.time = str(float(user_profile.time) + avg_time)

                user_profile.save()



                return JsonResponse(context, status=200)

            else:
                print("false")

                user_profile.chances_left =int(user_profile.chances_left)-1

                user_profile.save()

                update_leaderboard(request)


                if user_profile.chances_left == 0:

                    context = {"continue": "false", "tries": user_profile.chances_left}

                    request.session.flush()
                    request.session["done"]=1


                else:



                    context = {

                        'continue': "true",
                        "tries": user_profile.chances_left,

                        'level': user_profile.lvl,

                        'tries': user_profile.chances_left,

                        'filepath': "http://mysterydigits.vjec.in/" + request.session["filename"],

                    }



                return JsonResponse(context, status=400)



    except UserProfile.DoesNotExist:

        return JsonResponse({"message": "Phone number not registered."}, status=404)

def end(request):

    return render(request, "end.html")


def dashboard(request):
    if request.session.get("done"):
        return render(request, "login.html")

    phone = request.session.get("phone")

    if phone:

        user_profile = UserProfile.objects.get(phone=phone)



        if not request.session.get("generated"):

            digits_in_image = load_data_from_json("main/data.json")
            sanam=digits_in_image["level_"+str(user_profile.lvl)]
            r=random.randint(0,19)
            random_entry=sanam[r]
            filename = random_entry['filename']
            guessed_numbers = random_entry['guessed_numbers']

            string=""
            for i in guessed_numbers:
                string+=i

            request.session["generated"] = string
            request.session["filename"]=filename
            context = {

            'lvl': user_profile.lvl,

            'tries': user_profile.chances_left,

            'filename': "http://mysterydigits.vjec.in/" + str(filename),

            }


        else:
            context = {

            'lvl': user_profile.lvl,

            'tries': user_profile.chances_left,

            'filename': "http://mysterydigits.vjec.in/" + request.session["filename"],

            }




        request.session["time"] = time.time()

        update_leaderboard(request)



        return render(request, "dashboard.html", context)

    else:

        return render(request, "login.html")



def end(request):

    return render(request, "end.html")



def index(request):
    # Check if a session variable (e.g., 'user_id' or similar) exists
    if request.session.get('generated'):
        # Redirect to the dashboard if the user is logged in (session exists)
        return redirect('dashboard')  # Replace 'dashboard' with the actual name of your dashboard route
    else:
        # If no session, render the index page
        return render(request, 'index.html')



def setUp():

    UserProfile.objects.create(

        uid='1234567899',

        name='Ashish',

        phone='1234567899',

        time='0',

    )



def flush(request):

    request.session.flush()

    return JsonResponse({"message": "ok"}, status=200)



def login(request):

    #setUp()

    return render(request, 'login.html')



@require_POST

def get_details(request):

    phone = request.POST.get('phone')



    try:

        user_profile = UserProfile.objects.get(phone=phone)
        '''
        if user_profile.started == '1':
            return JsonResponse({"message": "User already started the game."}, status=400)
        user_profile.started = '1'
        '''

        user_profile.save()

        request.session['phone'] = phone



        return JsonResponse({"message": "Data received successfully"}, status=200)



    except UserProfile.DoesNotExist:

        return JsonResponse({"message": "Phone number not registered."}, status=404)

