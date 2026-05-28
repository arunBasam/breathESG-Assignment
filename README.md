# Breathe ESG

Breathe ESG is a full-stack ESG ingestion and analyst review platform built with Django REST Framework and React.

## Features

* Upload ESG source records
* Normalize raw data
* ESG Scope classification
* Approve / Reject review workflow
* Audit logging and history tracking
* Dashboard analytics
* CSV export
* Pagination, filtering, and sorting
* Multi-tenant architecture
* API versioning
* Automated tests with coverage

---

## Tech Stack

### Frontend

* React
* Vite
* Axios

### Backend

* Django
* Django REST Framework

### Database

* SQLite

### Deployment

* Frontend: Vercel
* Backend: Render

---

## Live Demo

### Frontend

https://breath-esg-assignment-taupe.vercel.app

### Backend API Docs

https://breathesg-assignment.onrender.com/api/v1/records/docs/

---

## Run Locally

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Testing

```bash
python manage.py test
```

Coverage:

```bash
coverage run manage.py test

coverage report
```

Current Coverage: **91%**

---

## API Endpoints

* `/api/v1/records/`
* `/api/v1/records/list/`
* `/api/v1/records/stats/`
* `/api/v1/records/quality/`
* `/api/v1/records/audit/`
* `/api/v1/records/docs/`

---

## Project Highlights

* Production deployment completed
* Backend and frontend fully integrated
* Real-time dashboard analytics
* RESTful API architecture
* Validation and duplicate prevention
* CI-style testing approach
