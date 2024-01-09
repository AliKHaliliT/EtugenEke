from sqlalchemy.orm import sessionmaker
from ...database.db.etugeneke_db import engine
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from ...database.models.admins import Admins
import bcrypt


Session = sessionmaker(bind=engine)

class AdminAuth(AuthenticationBackend):

    """
    
    This class is used to authenticate admins.
    
    """

    async def login(self, request: Request) -> bool:

        form = await request.form()
        request.session.update({"username": form["username"], "password": form["password"]})


        return await self.authenticate(request)
    

    async def authenticate(self, request: Request) -> bool:

        with Session() as session:

            admin = session.query(Admins).filter(Admins.username == request.session.get("username")).first()

            if admin: 
                if not bcrypt.checkpw(request.session.get("password").encode("utf-8"), admin.password.encode("utf-8")):
                    return False
                else:
                    request.session.update({"role": admin.role})
                    return True
            else:
                return False
            

    async def logout(self, request: Request) -> bool:
        request.session.clear()