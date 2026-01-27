from ..baseUsecase import BaseUsecase
from .constants import (
    extract_float,
    GC_BOOKING_REGEX,
    TVA_REGEX,
    AMOUNT_REGEX,
    AMOUNT_REGEX_WITH_SYMBOL
)
from domain.services.ocrService import OCRService
from domain.services.openaiService import OpenAIService
from application.dtos.invoiceDto import InvoiceCreateSchema
from domain.mappers.invoiceMapper import InvoiceMapper

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN
import pdfplumber
from io import BytesIO


class ProcessOCRFileUsecase(BaseUsecase):
    
    def __init__(
        self,
        ocrService: OCRService,
        openaiClientService: OpenAIService
    ) -> None:
        self.ocrService = ocrService
        self.openaiClientService = openaiClientService
    
    async def completion(self) -> any:
        return await self.openaiClientService._chat_client_completion(self.full_text)
    
    async def execute(self, file_bytes: bytes) -> any:
        
        texts, images = await self.ocrService.process_ocr_file(file_bytes)
        text = "\n".join(texts)
        
        self.full_text = text
        amounts = self.extract_amounts()
        tvas = self.extract_tva()
        tva, ht_amount, ttc_amount, tva_amount = self.predict_tva(tvas, amounts)
        tva_amount =  ttc_amount - ht_amount if ht_amount == tva_amount else tva_amount
        # openai_response = await self.completion()
        return self.full_text
        # return {
        #     "gc_booking": self.extract_gc_booking(),
        #     "chat_response": openai_response.content,
        #     "extracted_data": {
        #         "predicted_data": {
        #             "_tvas": tvas,
        #             "_amounts": amounts,
        #         },
        #         "openai_response": openai_response.content,
        #         "tva": tva,
        #         "montant_ttc": float(Decimal(ttc_amount).quantize(Decimal("0.01"))),
        #         "montant_ht": float(Decimal(ht_amount).quantize(Decimal("0.01"))),
        #         "montant_tva": float(Decimal(tva_amount).quantize(Decimal("0.01")))
        #     }
        # }
    
    def extract_gc_booking(self) -> str | None:
        gc_booking = GC_BOOKING_REGEX.search(self.full_text)
        if gc_booking:
            return gc_booking.group(0)
        return None
    
    def extract_amounts(self) -> list[float]:
        amounts = AMOUNT_REGEX.findall(self.full_text)
        amounts_symbol = AMOUNT_REGEX_WITH_SYMBOL.findall(self.full_text)
        global_amounts = amounts + amounts_symbol
        if amounts and len(amounts) > 0:
            global_amounts = [extract_float(amount.replace("€", "")) for amount in amounts]
        return global_amounts if global_amounts else [0]

    def extract_tva(self) -> list[float|None]:
        tva = TVA_REGEX.findall(self.full_text)
        if tva:
            tvas = [extract_float(tva) for tva in tva]
            return tvas
        return [20]
    
    def predict_tva(
        self,
        tvas: list[float],
        amounts: list[float]
    ) -> tuple[float, float, float]:
        print(tvas, amounts)
        ttc_amount = max(amounts)
        print('@ TTC AMOUNT', ttc_amount)
        default_tva = 20
        for tva in tvas:
            if tva == 0:
                continue
            
            ht_amount = ttc_amount / (1 + tva / 100)
            # 100 (ttc) => 80 (ht) => 20 (tva)
            if self.is_close(ht_amount, amounts):
                print('@ FIRST HT AMOUNT: ', tva, ht_amount, ttc_amount, ttc_amount - ht_amount)
                return tva, ht_amount, ttc_amount, ttc_amount - ht_amount
            
            ht_amount = ttc_amount / (1 + default_tva / 100)
            if self.is_close(ht_amount, amounts):
                print('@ SECOND HT AMOUNT: ', default_tva, ht_amount, ttc_amount, ttc_amount - ht_amount)
                return default_tva, ht_amount, ttc_amount, ttc_amount - ht_amount
        
            ht_amount = ttc_amount - tva
            if self.is_close(ht_amount, amounts):
                print('@ THIRD HT AMOUNT: ', default_tva, ht_amount, ttc_amount, ttc_amount - ht_amount)
                return 
            
        montant_tva = ttc_amount * ( 1 + default_tva / 100)
        if self.is_close(montant_tva, amounts):
            print('@ MONTANT TVA: ', default_tva, ttc_amount - montant_tva, ttc_amount, montant_tva)
            return default_tva, ttc_amount - montant_tva, ttc_amount, montant_tva
        
        else:
            print('@ DEFAULT MONTANT TVA: ', default_tva, ttc_amount * ( 1 + default_tva / 100 ), ttc_amount, montant_tva)
            return default_tva, ttc_amount * ( 1 + default_tva / 100 ), ttc_amount, montant_tva
        
    def is_close(self, value, values, tol=1e-2):
        return any(abs(value - v) < tol for v in values)
