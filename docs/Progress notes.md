# CNET ENERGY HUB

## Front-end
https://www.cenet.it/

## *Progress notes for website development*

# Week 1\. 23.03-29-03:

- Backend initialized using FastAPI   
  - (Python web framework used to build API)  
  - (Automatically generates API documentation)  
- SQLite database implemented (test.db)  
- Database connection set up with SQLAlchemy  
  - (A library used to interact with databases)  
  - (Used to define tables (for users) and store data in the database)  
- Automatic table creation configured  
- Project structured into modules (main.py, auth.py, models.py, schemas.py, database.py)  
- /register endpoint created for user registration  
- Password hashing implemented for security  
- Input validation handled using Pydantic schemas  
  - (Used for data validation and structure)  
  - (Ensures input data (e.g. email, password) is correct)  
- Backend running locally via Uvicorn  
  - (A server used to run the FastAPI application, starts backend locally)  
  - (Command for terminal:  uvicorn main:app \--reload)  
- API tested using Swagger UI (/docs)  
  - (Automatic API interface provided by FastAPI)  
  - (Lets you test endpoints directly in the browser)

# Week 2\. 13.04-19.04:

Test:

- [x] Register user works  
- [x] Login with user works  
- [x] Database saves data  
- Implemented a stable authentication and login system with testing  
- Added protection for user-specific data and basic access control  
- Enabled role-based registration with user, supplier, and operator accounts  
- Added initial backend structure for matching and simulations  
- Added profile retrieval and update functionality

# Week 3

1. 

# Week 4

1. 

# Week 5

1. 

