
Library Project in Django with Stripe

Description
This project is a Django-based web application that facilitates book transactions using Stripe API. 
Users can register as writers to post books for sale or as regular users to browse and purchase books.

Features
User Roles: Users can register as either writers or regular users.
Writer Functionality: Writers can upload books and set prices.
User Functionality: Users can browse books and make purchases.
Stripe Integration: Payment processing using the Stripe API.
Email Notifications: Users receive email notifications after purchasing a book.
Setup Instructions
Clone the repository


git clone https://github.com/your_username/library-project.git
cd library-project
Set up virtual environment (optional but recommended)


python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
Install dependencies

pip install -r requirements.txt
Set up Stripe API keys

Obtain your Stripe API keys from Stripe Dashboard.

Create a .env file in the root directory and add your keys:


STRIPE_TEST_SECRET_KEY=your_test_secret_key
STRIPE_TEST_PUBLIC_KEY=your_test_public_key
Run migrations

python manage.py migrate
Create a superuser (optional)

python manage.py createsuperuser
Start the development server

python manage.py runserver
Access the application

Open your web browser and go to http://localhost:8000 to view the application.

Usage
Register/Login: Users can register as writers or regular users.
Writer Dashboard: Writers can upload books and set prices.
User Dashboard: Users can browse available books, view details, and make purchases.
Payment: Users will be redirected to Stripe checkout for payment. After successful payment, they will receive an email notification.
Contributing
Contributions are welcome! Please follow these steps:
