=====
Game.Azelphur.com
=====

This is the (soon to be) source code to game.azelphur.com, we're powered by Python and Django along with Mezzanine and DjangoBB for the forums. Feel free to fix bugs or make improvements, or use this code for your own projects :)

Quick start
-----------

1. Create a virtual environment with `virtualenv env` and activate it `with source env/bin/activate`

2. Install the requirements with pip install -r requirements.txt

3. Copy game/local_settings.py.example to game/local_settings.py

4. Run `python manage.py migrate` to create the models

5. Start the development server with `python manage.py runserver`
   and visit http://127.0.0.1:8000/
