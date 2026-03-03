import httpx
from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.StorageGateway import StorageFileGateway
from typing import Any

class StorePDFInvoice(BaseActivity):
    def __init__(self, storage: StorageFileGateway):
        self.storage = storage
        
    async def execute(self, pdf_url: str, invoice_name: str) -> str:
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            
            response = await client.get(pdf_url)
            if response.status_code == 200:
                file_byte = response.content
                
            if file_byte:
                return await self.storage.upload_file(file_byte, invoice_name)
            else:
                return None