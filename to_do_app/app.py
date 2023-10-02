from fastapi import Depends, FastAPI
from to_do_app.api.router import router
from to_do_app.lifecycle import init_app
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
init_app(app)
app.router.include_router(router)    

 