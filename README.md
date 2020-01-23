# Address_app
	
This is for address maintenance app with user profile data, it uses the django admin User model and maintenance the different profile table. Whenever we are register the new user default profile data with given mobile number.It uses the post_save signals to create profile, for auth it uses the jwt token.

# Installation and Execution
#### Basic Requirements

	Python 3
	Virtualenv

#### step 1: create environment with virtualenv and activate

#### step 2: install the requirements with requirements.txt file located in project folder

       pip install -r requirements.txt
       
#### step 3: Create migration file with makemigration command

      python manage.py makemigrations

#### step 4:apply the migrations to db with migrate command
    
     python manage.py migrate
     
#### step 5:run the application

     python manage.py runserver



