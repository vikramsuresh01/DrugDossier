from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime

from pymongo import MongoClient

app = FastAPI()
templates = Jinja2Templates(directory="templates")      

# Define the directory path to the 'static' directory
current_dir = Path(__file__).resolve().parent
static_directory = current_dir / "static"   

# Serve static files (images, CSS, JavaScript, etc.) from the 'static' directory
app.mount("/static", StaticFiles(directory=static_directory), name="static")

client = MongoClient("mongodb+srv://vs7552:drugdossier@drugdossier.09fff1b.mongodb.net/user_info?retryWrites=true&w=majority")
db = client.user_info
collection = db.login_creds

db2 = client.substances
collection2 = db2.narcotics
collection3 = db2.prescriptions
collection4 = db2.supplements

db3 = client.reviews
collection5 = db3.review

authenticated_users = set()

def get_authenticated_users():
    return authenticated_users

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if request.client.host in authenticated_users:
        # If the user is authenticated, render a different template
        return templates.TemplateResponse("authenticated_home.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/narcotics.html", response_class=HTMLResponse)
async def read_narcotics(request: Request,authenticated_users: set = Depends(get_authenticated_users)):
    dataset = list(collection2.find({}))
    return templates.TemplateResponse("narcotics.html", {"request": request,"authenticated_users": authenticated_users,"dataset": dataset})

@app.get("/narcotics/{drug_name}.html", response_class=HTMLResponse)
async def read_substance(drug_name: str, request: Request, authenticated_users: set = Depends(get_authenticated_users)):
    # Fetch substance data from MongoDB based on the drug_name
    substance_data = collection2.find_one({"drug_name": drug_name})
    # Pass substance data to the template
    return templates.TemplateResponse("substance_page.html", {"request": request,"authenticated_users": authenticated_users,"substance_data": substance_data})

@app.get("/prescriptions/{drug_name}.html", response_class=HTMLResponse)
async def read_substance(drug_name: str, request: Request, authenticated_users: set = Depends(get_authenticated_users)):
    # Fetch substance data from MongoDB based on the drug_name
    substance_data = collection3.find_one({"drug_name": drug_name})
    # Pass substance data to the template
    return templates.TemplateResponse("substance_page.html", {"request": request,"authenticated_users": authenticated_users,"substance_data": substance_data})

@app.get("/supplements/{drug_name}.html", response_class=HTMLResponse)
async def read_substance(drug_name: str, request: Request, authenticated_users: set = Depends(get_authenticated_users)):
    # Fetch substance data from MongoDB based on the drug_name
    substance_data = collection4.find_one({"drug_name": drug_name})
    # Pass substance data to the template
    return templates.TemplateResponse("substance_page.html", {"request": request,"authenticated_users": authenticated_users,"substance_data": substance_data})

@app.get("/prescriptions.html", response_class=HTMLResponse)
async def read_prescriptions(request: Request,authenticated_users: set = Depends(get_authenticated_users)):
    dataset = list(collection3.find({}))
    return templates.TemplateResponse("prescriptions.html", {"request": request,"authenticated_users": authenticated_users,"dataset": dataset})

@app.get("/supplements.html", response_class=HTMLResponse)
async def read_supplements(request: Request,authenticated_users: set = Depends(get_authenticated_users)):
    dataset = list(collection4.find({}))
    return templates.TemplateResponse("supplements.html", {"request": request,"authenticated_users": authenticated_users,"dataset": dataset})

@app.get("/blog.html", response_class=HTMLResponse)
async def read_blog(request: Request,authenticated_users: set = Depends(get_authenticated_users)):
    return templates.TemplateResponse("blog.html", {"request": request,"authenticated_users": authenticated_users})

@app.get("/review.html", response_class=HTMLResponse)
async def read_review(request: Request,authenticated_users: set = Depends(get_authenticated_users)):
    if request.client.host in authenticated_users:
        # If the user is authenticated, render a different template
        return templates.TemplateResponse("review.html", {"request": request,"authenticated_users": authenticated_users})
    else:
        return templates.TemplateResponse("signin.html", {"request": request,"authenticated_users": authenticated_users})

@app.get("/login.html", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signin.html", response_class=HTMLResponse)
async def read_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

# Define the route for the login page
@app.get("/login.html", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/authenticated_home", response_class=HTMLResponse)
async def authenticated_home(request: Request):
    if request.client.host in authenticated_users:
        # If the user is authenticated, render a different template
        return templates.TemplateResponse("authenticated_home.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request})
    


# Define the root route to handle both GET and POST requests
@app.route("/authenticated_home", methods=["GET", "POST"])
async def read_root(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse("authenticated_home.html", {"request": request})
    elif request.method == "POST":
        return templates.TemplateResponse("authenticated_home.html", {"request": request})
        pass

# Define the route to handle login form submissions
@app.post("/login", response_class=HTMLResponse)
async def process_login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Process the login form data here
    # For demonstration purposes, let's just print the email and password
    print("Email:", email)
    print("Password:", password)
    collection.insert_one({"email": email, "password": password})
    authenticated_users.add(request.client.host)

    # Redirect to the home page after processing login
    return RedirectResponse(url="/authenticated_home")

# Define the route to handle logout
@app.get("/logout", response_class=RedirectResponse)
async def logout(request: Request):
    authenticated_users.discard(request.client.host)
    return RedirectResponse(url="/")

# Define the root route to handle both GET and POST requests
@app.route("/", methods=["GET", "POST"])
async def read_root(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse("index.html", {"request": request})
    elif request.method == "POST":
        return templates.TemplateResponse("index.html", {"request": request})
        pass

@app.post("/signin")
async def process_signin(request: Request,email: str = Form(...), password: str = Form(...)):
    # Check if the email and password combination exists in the database
    user = collection.find_one({"email": email, "password": password})
    if user:
        print("Success")
        authenticated_users.add(request.client.host)
        print(authenticated_users)
        return RedirectResponse(url="/authenticated_home")
    else:
        print("Fail")
        return templates.TemplateResponse("login.html", {"request": request, "error_message": "Wrong email or password."})
    
@app.post("/submit_review")
async def submit_review(request: Request, email: str = Form(...), substanceType: str = Form(...), drugName: str = Form(...), reviewText: str = Form(...)):
    # Create a new document with the form data
    review_doc = {
        "email": email,
        "substanceType": substanceType,
        "drugName": drugName,
        "reviewText": reviewText,
        "timestamp": datetime.utcnow()
    }

    # Insert the document into the MongoDB collection
    collection5.insert_one(review_doc)

    # Return a response indicating success
    return templates.TemplateResponse("authenticated_home.html", {"request": request})

@app.get("/reviews.html", response_class=HTMLResponse)
async def get_reviews(request: Request):
    # Fetch reviews from MongoDB
    if request.client.host in authenticated_users:
        reviews = list(collection5.find({}))
        return templates.TemplateResponse("reviews.html", {"request": request, "reviews": reviews,"authenticated_users": authenticated_users})
    else:
        return templates.TemplateResponse("signin.html", {"request": request,"authenticated_users": authenticated_users})
    

