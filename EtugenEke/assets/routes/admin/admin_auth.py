from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from ...database.models.admins import Admins
import bcrypt


Session = sessionmaker(bind=engine)

class AdminAuth(AuthenticationBackend):

    """

    Authentication backend for admin users.

    This class handles authentication for administrators by implementing
    login, authentication, and logout functionality. It utilizes session-based 
    authentication and password hashing for security.

    
    Methods
    -------
    login():
        Authenticates an admin user based on form data and stores session details.

    authenticate():
        Verifies the provided credentials against the stored admin records.

    logout():
        Clears the session to log out the admin user.

    """

    async def login(self, request: Request) -> bool:

        """

        Handles admin login.
        Extracts username and password from the request form, updates the session, 
        and attempts authentication.

        
        Parameters
        ----------
        request : Request
            The incoming request containing authentication data.

            
        Returns
        -------
        response : bool
            `True` if authentication succeeds, `False` otherwise.

        """

        form = await request.form()
        request.session.update({"username": form["username"], "password": form["password"]})


        return await self.authenticate(request)


    async def authenticate(self, request: Request) -> bool:

        """

        Authenticates the admin user.
        Fetches the admin record from the database using the username stored in the session.
        Verifies the password using bcrypt.

        Parameters
        ----------
        request : Request
            The request containing session data.

            
        Returns
        -------
        response : bool
            `True` if authentication succeeds, `False` otherwise.

        """

        with Session() as session:
            admin = session.query(Admins).filter(Admins.username == request.session.get("username")).first()

            if admin:
                if not bcrypt.checkpw(request.session.get("password").encode("utf-8"), admin.password.encode("utf-8")):
                    return False
                request.session.update({"role": admin.role})
                return True
            return False


    async def logout(self, request: Request) -> bool:

        """

        Logs out the admin user.
        Clears the session to remove authentication data.


        Parameters
        ----------
        request : Request
            The request containing session data.

            
        Returns
        -------
        response : bool
            Always returns True.
        
        """

        request.session.clear()


        return True