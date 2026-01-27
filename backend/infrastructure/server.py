from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from application.containers.appContainer import AppContainer
from infrastructure.db.engine import init_models
from infrastructure.router import RouterHandler

def bootstrap() -> FastAPI:
    
    container = AppContainer()
    container.init_resources()
    
    settings = container.config

    
    print(settings.application_name())
    print(settings.database_uri())
    
    app = FastAPI(
        title=settings.application_name(),
        version=settings.application_version(),
        description=settings.application_description(),
    )
    app.container = container
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    api_router = APIRouter(prefix="/api")
    
    router_handler = RouterHandler(api_router)
    router_handler = router_handler.load_routers()
    app.include_router(router_handler)
    app.include_router(api_router)
    
    container.wire(
        packages=["infrastructure.routes"]   # <<< ajout obligatoire
    )
    
    @app.on_event("startup")
    async def startup_event():
        await init_models()
        print("✅ App démarrée (async)")

    @app.on_event("shutdown")
    async def shutdown_event():
        print("🛑 App arrêtée proprement")
        
    return app