import logging
from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from ...models.user import User
from ...database.models.users import Users
from ...database.models.plans import Plans
from fastapi.responses import JSONResponse, Response
from ...utils.is_valid_email import is_valid_email
import dns.resolver
import bcrypt
from datetime import datetime


# Configure logging
logging.basicConfig(level=logging.DEBUG) 

file_handler = logging.FileHandler(r'logs\signup.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger('').addHandler(file_handler)


router = APIRouter()
Session = sessionmaker(bind=engine)

@router.post("/actions/signup/")
async def signup(user: User) -> JSONResponse:

    """
    
    This endpoint registers a user based on provided credentials.


    Parameters
    ----------
    user : User
        A model object containing user details for registration.


    Returns
    -------
    response: JSONResponse
        A JSON response containing the status of the registration request.
    
    """

    logging.info(f"Received: {user} as payload")

    try:

        with Session() as session:
            
            # Check if the user exists based on username or email
            user_exists = session.query(Users).filter(
                (Users.username == user.username) | (Users.email == user.email)
            ).first()

            if user_exists:
                logging.error(f"User {user.username} already exists")
                return JSONResponse(content={"message": "User already exists"}, status_code=400)


            # Check email validity
            if not is_valid_email(user.email):
                logging.error(f"User {user.username} entered invalid email")
                return JSONResponse(content={"message": "Invalid email"}, status_code=400)
            
            domain = user.email.split('@')[-1]
            dns.resolver.resolve(domain, "MX")


            # Set the credit based on the plan
            plans = session.query(Plans).filter(Plans.plan == user.plan).first()

            if not plans:
                logging.error(f"Plan {user.plan} does not exist")
                return JSONResponse(content={"message": "Plan does not exist"}, status_code=400)
            
            credit = plans.credit
            

            hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

            # Create the user object and add it to the database
            new_user = Users(
                date_created=datetime.utcnow(),
                role="user",
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                password=hashed_password.decode("utf-8"),
                plan=user.plan,
                credit=credit,
                recharged=False,
                token=''
            )
            session.add(new_user)

            session.commit()


            logging.info(f"User {user.username} registered successfully")
            return JSONResponse(content={"message": "User registered successfully"}, status_code=200)
    except dns.resolver.NXDOMAIN:
        logging.error(f"User {user.username} entered invalid email")
        return JSONResponse(content={"message": "Invalid email"}, status_code=400)
    except Exception as e:
        logging.error(f"Error in registration: {e}", exc_info=True)
        return Response(status_code=500)