from temporalio import activity

class SayHelloActivity:
    
    @activity.defn(name="say_hello")
    async def execute(self, name: str) -> str:
        return f"Hello, {name}! from say hello activity"