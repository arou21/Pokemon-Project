from app import app
from flask import render_template, request, redirect, url_for
from .pok_API import get_pokemon, get_battle_points
from .forms import UserCreationForm, PoknameForm, LoginForm, ProfileForm, CatchForm, BattleForm, ReleaseForm
from .models import User, caught_pokemon, Pokemon_table
from flask_login import login_user, current_user, logout_user


@app.route('/')
def homePage():
    people = ['name', "Brandt", "Aubrey", "Nicole"]
    text = "SENDING THIS FROM PYTHON!!!"
    return render_template('index.html', people=people, my_text=text, user=current_user)


@app.route('/catch', methods=["GET", "POST"])
def catch():
    form = CatchForm()
    if request.method == 'POST':
        if form.validate():
            # Check if user has 5 pokemon already
            my_pokemon = caught_pokemon.query.filter_by(user_id=current_user.id).all()
            if my_pokemon and len(my_pokemon) >= 5:
                return render_template('catch.html', form=form, message="You already have 5 pokemon!")

            pokname = form.pokname.data
            result = get_pokemon(pokname)
            # Check if we were able to find a Pokemon
            if result:
                name, ability, base_experience, image = result
                caught = caught_pokemon(name, current_user.id, shiny=False)
                caught.saveToDB()

                poke = Pokemon_table(name, base_experience, ability, 100, 100, 100)
                poke.saveToDB()

                message = "You caught the "+name+"!"
                return render_template('catch.html', form=form, message=message, name=name, ability=ability, base_experience=base_experience, image=image)
            else:
                return render_template('catch.html', form=form, message="Could not find that pokemon")

    return render_template('catch.html', form=form)
    # if form.validate():


@app.route('/searchPage', methods=["GET", "POST"])
def searchPage():
    catchForm = CatchForm()
    form = PoknameForm()
    pokname = ""
    if request.method == 'POST':
        if form.validate():
            pokname = form.pokname.data
            name, ability, base_experience, image = get_pokemon(pokname)
            return render_template('search.html', form=form, catchForm=catchForm, name=name, ability=ability, base_experience=base_experience, image=image)
    return render_template('search.html', form=form, catchForm=catchForm)


@app.route('/signup', methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            user_name = form.user_name.data
            email = form.email.data
            password = form.password.data

            print(first_name, email, password)

            # add user to database
            user = User(first_name, last_name, user_name, email, password)
            print(user)

            user.saveToDB()

            # return render_template('signup.html', form = form )
            return redirect(url_for('loginPage'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def loginPage():
    form = LoginForm()
    error = ''
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user:
                if user.password == password:
                    login_user(user)
                    return redirect("/", code=302)

                else:
                    error = 'wrong password'

            else:
                error = 'username does not exist'
        else:
            error = 'invald form'

    return render_template('login.html', form=form, error=error)


@app.route('/logout', methods=["GET"])
def logoutRoute():
    logout_user()
    return redirect(url_for("homePage"), code=302)

@app.route('/profile', methods=["GET", "POST"])
def profile_page():
    form = ProfileForm()
    releaseForm = ReleaseForm()
    pokemon = caught_pokemon.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        print(releaseForm.pokemon.data)
        released_pokemon = caught_pokemon.query.filter_by(id=releaseForm.pokemon.data).first()
        pokemon_after_release = []
        for p in pokemon:
            if p.id != released_pokemon.id:
                pokemon_after_release.append(p)
        released_pokemon.deleteFromDB()
        return render_template('profile.html', form=form, releaseForm=releaseForm, pokemon=pokemon_after_release)
    return render_template('profile.html', form=form, releaseForm=releaseForm, pokemon=pokemon)

@app.route('/battle', methods=["GET", "POST"])
def battle():
    form = BattleForm()
    # Check for opponents, everyone who is not the current user
    opponents = []
    opp_users = User.query.filter(User.id != current_user.id).all()
    for user in opp_users:
        pokemon = caught_pokemon.query.filter_by(user_id=user.id).all()
        opponents.append({
            "id": user.id,
            "user_name": user.user_name,
            "pokemon": pokemon
        })

    if request.method == "POST":
        opponent = User.query.filter_by(id=form.opponent.data).first()
        opponent_pokemon = caught_pokemon.query.filter_by(user_id=opponent.id).all()
        my_pokemon = caught_pokemon.query.filter_by(user_id=current_user.id).all()
        opponent_points = get_battle_points(opponent_pokemon)
        my_points = get_battle_points(my_pokemon)
        if my_points >= opponent_points:
            message = "You won the battle against "+opponent.user_name+"!"
        else:
            message = "You lost the battle against "+opponent.user_name+"!"
        return render_template('battle.html', form=form, opponents=opponents, user=current_user, message=message)
    return render_template('battle.html', form=form, opponents=opponents, user=current_user)

