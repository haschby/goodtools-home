from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from application.containers.appContainer import AppContainer
from infrastructure.router import RouterHandler
from infrastructure.middleware.routeLoggerMiddleware import RouteLoggerMiddleware
from contextlib import asynccontextmanager

from domain.models.baseModel import BaseMain, GCBase

def create_lifespan():

    @asynccontextmanager
    async def lifespan(app: FastAPI):

        container = app.state.container

        await container.main_db_uri().init_models(BaseMain)
        # await container.gc_db_uri().init_models()

        container.logger().info(
            "Database initialized"
        )

        yield

        container.logger().info(
            "Application shutdown"
        )

    return lifespan

    

def bootstrap() -> FastAPI:
    
    container = AppContainer()
    container.init_resources()

    settings = container.settings()
    
    app = FastAPI(
        title=settings.application_name,
        version=settings.application_version,
        description=settings.application_description,
        lifespan=create_lifespan(),
    )
    
    app.state.container = container
    
    app.add_middleware(
        RouteLoggerMiddleware,
        logger=container.logger()
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    base_router = APIRouter(prefix="/api")
    router = RouterHandler(base_router, container.logger())
    router.load_routers()
    app.include_router(
        base_router
    )
    
    container.wire(
        packages=["infrastructure.routes"]   # <<< ajout obligatoire    
    )
        
    return app