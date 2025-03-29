XeroWaste/
│── backend/
│   ├── app/
│   │   ├── __init__.py          # Initialize Flask app
│   │   ├── models.py            # SQLAlchemy models (DB schema)
│   │   ├── routes.py            # API endpoints
│   │   ├── utils.py             # Helper functions
│   │   ├── config.py            # Database & app configuration
│   │   ├── ai/                  # AI/ML models (if needed)
│   │   │   ├── inventory_model.py
│   │   │   ├── waste_prediction.py
│   │   ├── static/               # Static files (images, CSS, JS)
│   │   ├── templates/            # HTML templates (if using Jinja2)
│── migrations/                    # Flask-Migrate (for DB migrations)
│── tests/                         # Unit tests
│── .gitignore                      # Ignore unnecessary files
│── requirements.txt                # Python dependencies
│── run.py                          # Flask entry point
│── README.md                       # Project documentation