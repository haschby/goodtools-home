from dependency_injector import containers, providers
from infrastructure.db.userRepository import UserRepositoryImpl

class UserContainer(containers.DeclarativeContainer):
    postgres = providers.Dependency()
    
    repository = providers.Factory(
        UserRepositoryImpl,
        session=postgres
    )