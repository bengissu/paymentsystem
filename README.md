# Payment System

This is a fully functional payment system application built with Django, designed to facilitate secure money transfers, currency conversion, and transaction requests between registered users. The project focuses on providing a seamless user experience, ensuring data security, and demonstrating key web development skills. It also includes an admin panel for managing users and transactions.

## Purpose of the Project

The purpose of this project is to showcase a complete web-based payment solution, where users can register, authenticate, and securely send/request money from others. It demonstrates strong backend development skills in Django, user authentication, currency conversion, and secure transaction handling. The project also illustrates frontend skills through a clean and responsive user interface.

This project is ideal for those looking for a robust solution for handling multi-currency transactions with a focus on security and extensibility. The architecture and code quality are designed with scalability and performance in mind.

## Key Features

### 1. **User Authentication & Authorization**:
   - **Registration**: Users can register with their details (name, email, username, password, and preferred currency).
   - **Login & Logout**: Only registered users can access the system, ensuring secure access to the platform.
   - **Role-based Access**: Regular users can access their own transactions, while admins can manage users and view all transactions.

### 2. **Transaction Management**:
   - **Send Money**: Users can securely send money to other registered users by entering the recipient's details. Transactions are automatically converted between currencies based on the latest exchange rates.
   - **Request Money**: Users can request money from others. The recipient can approve or deny the request, and the balance will be updated accordingly.
   - **Transaction History**: Users can view their complete transaction history, including sent, received, and pending requests.

### 3. **Currency Conversion**:
   - The application supports automatic currency conversion between USD, GBP, and EUR using preset exchange rates.
   - Conversion rates are flexible and can be easily modified in the `settings.py` file.

### 4. **Admin Panel**:
   - **User Management**: Admins can view and manage all user accounts, including the ability to create new users and administrators.
   - **Transaction Monitoring**: Admins can oversee all payment transactions, providing an overview of the system's activity.

### 5. **Security Features**:
   - **CSRF Protection**: The system is protected against Cross-Site Request Forgery.
   - **XSS Protection**: Cross-Site Scripting vulnerabilities are mitigated through input validation.
   - **SQL Injection Prevention**: The application uses Django’s ORM to protect against SQL injection attacks.
   - **Authentication Control**: Users must be authenticated to access sensitive actions such as sending or requesting money.

### 6. **Responsive Design**:
   - The front-end of the application is designed with a mobile-first approach, ensuring a smooth user experience across different devices.
   - User-friendly navigation for both users and admins with clear actions like "Send Money" and "Request Money" available on the homepage.

### 7. **RESTful Web Services**:
   - The application implements RESTful web services to return exchange rates between currencies or provide appropriate HTTP status codes when an unsupported currency is requested.

### 8. **Scalability & Extensibility**:
   - The project is designed with scalability in mind. New features, such as additional currencies or payment methods, can be integrated with minimal changes.
   - The system can be easily extended to support other functionalities like international payment gateways or multi-factor authentication.

### 9. **Error Handling**:
   - The application provides informative feedback for common issues such as insufficient balance, user not found, and incorrect details during money transfer.

## Project Structure

```
.
├── payapp/                  # The core Django app for payment functionality
│   ├── migrations/          # Database migrations
│   ├── admin.py             # Admin panel settings
│   ├── apps.py              # Application configuration
│   ├── forms.py             # Form handling for user inputs
│   ├── models.py            # Database models for users, transactions, etc.
│   ├── tests.py             # Unit tests for the application
│   └── views.py             # Handles HTTP requests and renders responses
├── paymentsystem/           # Main Django project folder
│   ├── asgi.py              # ASGI configuration
│   ├── settings.py          # Django settings (contains exchange rates)
│   ├── urls.py              # URL routing for the application
│   ├── wsgi.py              # WSGI configuration
├── register/                # Registration app for handling user sign-up
│   ├── migrations/          # Database migrations
│   ├── admin.py             # Admin configuration for user registrations
│   ├── apps.py              # App configuration
│   ├── forms.py             # Form handling for registrations
│   ├── models.py            # Models for user registration and profiles
│   ├── tests.py             # Unit tests for registration features
│   └── views.py             # Views for registration-related pages
├── templates/               # HTML templates
│   ├── payapp/
│   │   ├── homepage.html    # Homepage after login
│   │   ├── notifications.html  # Notifications for transaction requests and status
│   │   ├── request_money.html   # Page to request money
│   │   └── send_money.html   # Page to send money
│   ├── register/
│   │   ├── login.html        # Login page
│   │   └── register.html     # User registration page
└── .gitignore               # Files and directories to ignore in version control
```

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3
- **Database**: PostgreSQL (or any Django-supported database)
- **Security**: Django’s built-in security features for authentication and protection against XSS, CSRF, and SQL Injection.
- **APIs**: RESTful web services for currency conversion.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/paymentsystem.git
   cd paymentsystem
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```
   python manage.py migrate
   ```

4. Run the server:
   ```
   python manage.py runserver
   ```

5. Visit the site:
   - Login page: `http://127.0.0.1:8000/accounts/login/`
   - Registration page: `http://127.0.0.1:8000/accounts/register/`

## License

This project is licensed under the MIT License.
