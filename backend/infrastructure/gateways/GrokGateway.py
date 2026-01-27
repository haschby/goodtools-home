from xai_sdk import AsyncClient
from xai_sdk.chat import user
from application.dtos.gateway import OpenAIResponse
import json
from domain.ports.openaiGateway import OpenAIGateway

class GrokGateway(OpenAIGateway):
    
    prompt = """
    Extract the following fields from the French invoice below and return ONLY valid JSON:
    
    {{
    "gc_booking": "GC - Number",
    "invoice_number": "" (N° facture / Facture / Pièce n° / Facture n° / Part n°),
    "invoice_date": "",
    "amount_ht": 0,
    "amount_ttc": 0,
    "amount_tva": 0,
    "issuer_name": "",
    "construction_site_address": "" (Address where the work is carried out),
    }}
    
    Invoice: {invoice_text}
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = AsyncClient(
            api_key=self.api_key
        )
    
    async def chat_completion(self, message: str) -> OpenAIResponse:
        prompt = self.prompt.format(invoice_text=message)
        chat = self.client.chat.create(
            model=self.model,
            messages=[],
            response_format="json_object"
        )
        chat.append(user(prompt))
        response = await chat.sample()
        return OpenAIResponse(content=json.loads(response.content))