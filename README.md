# E-commerce-api
A FastAPI backend for managing users, products, payments, and orders. Sends order details and verification emails integrates with Gmail, supports admin roles, and demonstrates real-world API, database, and email automation in a clean, easy-to-understand structure.


## Features

- User authentication & role-based access (admin & regular users)  
- Product management (CRUD)  
- Order management (create, update, view orders)  
- Payment tracking  
- Sends emails for order details and verification codes  

---

## Requirements

- Python 3.10+  
- Git  

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/MoHanyy6/E-commerce-api.git
cd E-commerce-api

2. **Create a virtual environment**

python -m venv env

3. **Activate the virtual environment**
  Windows (PowerShell):  .\env\Scripts\Activate.ps1
  Windows (CMD):        .\env\Scripts\activate
  Linux/macOS:          source env/bin/activate

4. **Install dependencies**
  pip install -r requirements.txt


5. **Create .env file in the project root with your environment variables**
  DATABASE_URL=sqlite:///./test.db  # or your DB connection
  EMAIL_USER=your_email@gmail.com
  EMAIL_APP_PASSWORD=your_email_APP_password

6.**Run database migrations (if using Alembic):**
  alembic upgrade head


7. **Run the FastAPI server**
  uvicorn app.main:app --reload

8. **Access API**
  Open your browser and go to:      http://127.0.0.1:8000/docs
