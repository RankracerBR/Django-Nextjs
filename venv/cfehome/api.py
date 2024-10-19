from ninja import NinjaAPI, Schema

from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("/waitlists/", "waitlists.api.router")


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # if not request.user.is_authenticated
    email: str = None


@api.get("/hello")
def hello(request):
    print(request)
    return {"message": "Hello World"}

# instead of just using @login_required(), it is using auth=JWTAuth()
@api.get("/me", 
         response=UserSchema, 
         auth=JWTAuth())
def me(request):
    return request.user