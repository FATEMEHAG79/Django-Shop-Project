# Django Shop Project

This Django shop project is designed to create a comprehensive e-commerce platform with features for managing customers, products, orders, discounts, and more.

## Features

- **Customers:** Registration, profile management, address management
- **Products:** Add, edit, delete products and categories, apply discounts
- **Orders:** Add to cart, edit cart, place orders
- **Admin Panel:** Customized admin panel with different access levels (Manager, Supervisor, Operator)
- **Core:** Shared utilities and base models for the project

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Perform database migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the admin panel at `http://localhost:8000/admin/` to manage products, categories, customers, orders, etc.
- Customers can register, manage their profiles, addresses, and view order history.
- Products can be browsed, added to cart, and orders can be placed.
- Custom access levels in the admin panel allow different roles to perform specific actions.

## Tests

To run the tests, use the following command:
```bash
python manage.py test
```

## Contributors

- A Shop Website Designed In DJANGO : FATEMEH AGHAIE

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
