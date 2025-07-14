> A CS degree project by two first-year students. WareHub is a digital Sales and Inventory Management System built for small to large scale retail businesses.



## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Screenshots](#screenshots)
- [Configuration](#configuration)


## About

This project was made using Django, HTML, CSS and Javascript. Primarily, this project is for a first-year semester module that both collaborators are taking as part of our university course. The entire project was built in 2.5 months of work.



## Features

- Item barcode/qr code scanning using IP webcam
- Inventory tracking and control
- Role-based user access and management
- Automatic email-sending capabilities
- Automatic QR and Barcode generation for products
- Sales and inventory report generation
- Cashier POS system
- Transaction history and receipt generator
- Current active user list
- Password reset and first-time login password change




## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/JBroook/ALL-2
cd ALLProject
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to view the app.



## Screenshots

| Example | Description |
|--|-|
| <img width="800" height="450" alt="image" src="https://github.com/user-attachments/assets/d0c058ac-d8f3-40f2-99e1-5ae773e55034" /> | Inventory Page |
| <img width="800" height="450" alt="image" src="https://github.com/user-attachments/assets/2cd8818a-c9af-417a-a84b-338541bbef8c" /> | Login |
| <img width="800" height="450" alt="image" src="https://github.com/user-attachments/assets/1631a71a-411b-49be-a6c8-5f1ae5a1d3d7" /> | Home |
| <img width="800" height="450" alt="image" src="https://github.com/user-attachments/assets/bf80bb48-19d1-4141-8d96-5ed624b7855a" /> | Sales Dashboard |


## Configuration

```env
EMAIL_USER = 'youremail@gmail.com'
EMAIL_PASSWORD = 'App password here' 
```
