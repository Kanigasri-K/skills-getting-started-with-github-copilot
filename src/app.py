"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice and compete in interschool soccer matches",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim training, stroke improvement, and lap practice",
        "schedule": "Tuesdays, Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and mixed media projects",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Rehearse scenes, perform plays, and build acting skills",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "jack@mergington.edu"]
    },
    "Book Club": {
        "description": "Discuss books, share ideas, and explore literature",
        "schedule": "Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["sophia@mergington.edu", "ethan@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["olivia@mergington.edu", "mason@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice basketball skills and compete in school matches",
        "schedule": "Tuesdays, Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["evelyn@mergington.edu", "logan@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Improve volleyball techniques and play team drills",
        "schedule": "Wednesdays, Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["william@mergington.edu", "harper@mergington.edu"]
    },
    "Photography Club": {
        "description": "Explore photography, composition, and storytelling through images",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["elijah@mergington.edu", "ella@mergington.edu"]
    },
    "Ceramics Class": {
        "description": "Create pottery and learn hand-building and glazing techniques",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["henry@mergington.edu", "scarlett@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts as a team",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["grace@mergington.edu", "jackson@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice public speaking and compete in debate tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isla@mergington.edu", "sebastian@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if student already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Check participant limit
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not registered for this activity")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
