from sqladmin import ModelView
from ...database.models.users import Users
from ...database.models.lameness_detection_data import LamenessDetectionData
from ...database.models.lameness_detection_videos import LamenessDetectionVideos
from ...database.models.services import Services
from ...database.models.plans import Plans
from ...database.models.admins import Admins
from starlette.requests import Request


# Create model view for Users
class Users(ModelView, model=Users):
    name = "User"
    icon = "fas fa-user"
    column_list = ["id", "date_created", "role", "first_name", "last_name", "username", "email", "password", "plan", "recharged", "credit", "token"]
    column_default_sort = ("id", True)
    column_sortable_list = ["id", "date_created", "role", "first_name", "last_name", "username", "email", "password", "plan", "recharged", "credit", "token"]
    column_searchable_list = ["id", "date_created", "role", "first_name", "last_name", "username", "email", "password", "plan", "recharged", "credit", "token"]
    column_formatters = {Users.first_name: lambda m, a: m.first_name[:10] + "..." if len(m.first_name) > 10 else m.first_name, 
                         Users.last_name: lambda m, a: m.last_name[:10] + "..." if len(m.last_name) > 10 else m.last_name,
                         Users.username: lambda m, a: m.username[:10] + "..." if len(m.username) > 10 else m.username,
                         Users.email: lambda m, a: m.email[:10] + "..." if len(m.email) > 10 else m.email,
                         Users.password: lambda m, a: m.password[:10] + "..." if len(m.password) > 10 else m.password,
                         Users.plan: lambda m, a: m.plan[:10] + "..." if len(m.plan) > 10 else m.plan,
                         Users.token: lambda m, a: m.token[:10] + "..." if len(m.token) > 10 else m.token
    }
    save_as = True

# Create model view for LamenessDetection
class LamenessDetection(ModelView, model=LamenessDetectionData):
    name_plural = "Lameness Detection Data"
    icon = "fas fa-database"
    category = "Lameness Detection"
    column_list = ["id", "username", "date", "healthy", "lame", "fir", "uncertain"]
    column_default_sort = ("id", True)
    column_sortable_list = ["id", "username", "date", "healthy", "lame", "fir", "uncertain"]
    column_searchable_list = ["id", "username", "date", "healthy", "lame", "fir", "uncertain"]
    column_formatters = {LamenessDetectionData.username: lambda m, a: m.username[:10] + "..." if len(m.username) > 10 else m.username}
    save_as = True

# Create model view for LamenessDetectionVideos
class LamenessDetectionVideos(ModelView, model=LamenessDetectionVideos):
    name = "Lameness Detection Video"
    icon = "fas fa-video"
    category = "Lameness Detection"
    column_list = ["id", "username", "date_uploaded", "file", "lameness_status"]
    column_default_sort = ("id", True)
    column_sortable_list = ["id", "username", "date_uploaded", "file", "lameness_status"]
    column_searchable_list = ["id", "username", "date_uploaded", "file", "lameness_status"]
    column_formatters = {LamenessDetectionVideos.username: lambda m, a: m.username[:10] + "..." if len(m.username) > 10 else m.username,
                         LamenessDetectionVideos.file: lambda m, a: m.file[:30] + "..." if len(m.file) > 10 else m.file,
                         LamenessDetectionVideos.lameness_status: lambda m, a: m.lameness_status[:10] + "..." if len(m.lameness_status) > 10 else m.lameness_status
    }
    save_as = True

# Create model view for Services
class Services(ModelView, model=Services):
    name = "Service"
    icon = "fas fa-server"
    column_list = ["id", "date_added", "service_name", "service_description", "service_image"]
    column_default_sort = ("id", True)
    column_sortable_list = ["id", "date_added", "service_name", "service_description", "service_image"]
    column_searchable_list = ["id", "date_added", "service_name", "service_description", "service_image"]
    column_formatters = {Services.service_name: lambda m, a: m.service_name[:10] + "..." if len(m.service_name) > 10 else m.service_name,
                         Services.service_description: lambda m, a: m.service_description[:30] + "..." if len(m.service_description) > 10 else m.service_description
    }
    save_as = True


# Create model view for Plans
class Plans(ModelView, model=Plans):
    name = "Plan"
    icon = "fas fa-money-check-alt"
    column_list = ["id", "date_created", "plan", "credit", "price", "services", "description"]
    column_default_sort = ("id", True)
    column_sortable_list = ["id", "date_created", "plan", "credit", "price", "services", "description"]
    column_searchable_list = ["id", "date_created", "plan", "credit", "price", "services", "description"]
    column_formatters = {Plans.plan: lambda m, a: m.plan[:10] + "..." if len(m.plan) > 10 else m.plan,
                         Plans.credit: lambda m, a: m.credit[:10] + "..." if len(m.credit) > 10 else m.credit,
                         Plans.price: lambda m, a: m.price[:10] + "..." if len(m.price) > 10 else m.price,
                         Plans.services: lambda m, a: m.services[:10] + "..." if len(m.services) > 10 else m.services,
                         Plans.description: lambda m, a: m.description[:30] + "..." if len(m.description) > 10 else m.description
    }
    save_as = True


# Create model view for Admins
class Admins(ModelView, model=Admins):

    name = "Admin"
    icon = "fas fa-user-shield"
    column_list = ["id", "date_created", "first_name", "last_name", "username", "email", "password"]
    column_default_sort = ("id", True)
    column_sortable_list = ["id", "date_created", "first_name", "last_name", "username", "email", "password"]
    column_searchable_list = ["id", "date_created", "first_name", "last_name", "username", "email", "password"]
    column_formatters = {Admins.first_name: lambda m, a: m.first_name[:10] + "..." if len(m.first_name) > 10 else m.first_name, 
                         Admins.last_name: lambda m, a: m.last_name[:10] + "..." if len(m.last_name) > 10 else m.last_name,
                         Admins.username: lambda m, a: m.username[:10] + "..." if len(m.username) > 10 else m.username,
                         Admins.email: lambda m, a: m.email[:10] + "..." if len(m.email) > 10 else m.email,
                         Admins.password: lambda m, a: m.password[:10] + "..." if len(m.password) > 10 else m.password
    }
    save_as = True


    def is_accessible(self, request: Request) -> bool:
        return request.session.get("role") == "root"