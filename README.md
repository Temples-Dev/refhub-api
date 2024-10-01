# RefHub API

RefHub (Refreshinery Hub) is an internal API designed to manage the ordering of food by staff. The system allows staff to log in, enter their food orders with item names and prices, and an additional transportation fee is charged. The API also supports generating a consolidated PDF of all orders for the admin. Integration with Paystack is included for payment processing.

## Features

- Staff can log in and submit food orders (item and price).
- A fixed transportation charge is applied to all orders.
- Admin can view all orders and generate a PDF report with staff names and orders.
- Paystack payment integration for handling payments.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Payment**: Paystack API
- **API Documentation**: Swagger (using drf-yasg)
- **PDF Generation**: ReportLab (for creating the PDF of orders)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Temples-Dev/refhub-api.git
   cd refhub-api
   ```

2. Install **pipenv** if you don't have it:

   ```bash
   pip install pipenv
   ```

3. Install the required dependencies:

   ```bash
   pipenv install
   ```

4. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

5. Run database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Configuration

### Paystack Integration

To enable Paystack for payment processing, you'll need to add your Paystack secret key to the Django settings.

In `settings.py`, add the following:

```python
PAYSTACK_SECRET_KEY = "your-paystack-secret-key"
```

### Swagger API Documentation

Swagger documentation is automatically generated. To access the API documentation, navigate to:

```
http://localhost:8000/swagger/
```

## API Endpoints

- **Order Entry**:  
  `POST /api/orders/`  
  Staff can submit an order with an item name and price.

- **View All Orders** (Admin only):  
  `GET /api/orders/`  
  Admin can view all orders and generate a PDF report.

- **Generate PDF Report**:  
  `GET /api/orders/pdf/`  
  Generates a PDF report of all orders with staff names.

- **Paystack Payment**:  
  `POST /api/payment/`  
  Handles payment via Paystack.

## Running Tests

To run tests:

```bash
python manage.py test
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

