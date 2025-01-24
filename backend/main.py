from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from raspberry_interactions import ServerCommunications, RaspberryMsgHandling
from database import Base, engine
from routers import router

Base.metadata.create_all(bind=engine)

talk_to_raspberries = ServerCommunications()
msg_handling = RaspberryMsgHandling()

talk_to_raspberries.set_on_terminal_msg(msg_handling.on_terminal_msg)
talk_to_raspberries.set_on_checkout_msg(msg_handling.on_checkout_msg)


@asynccontextmanager
async def lifespan(_: FastAPI):
    talk_to_raspberries.on_start()
    yield
    talk_to_raspberries.on_cleanup()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "*",  # probably should do some better matching but w/e ig
]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
