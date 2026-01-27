import base64
import numpy as np
import cv2
from PIL import Image
from pdf2image import convert_from_bytes
from pytesseract import pytesseract
import easyocr
from io import BytesIO

from domain.ports.StorageGateway import StorageFileGateway
from application.usecases.ocr.constants import GOODCOLLECT_REGEX, ADDRESS_REGEX
from application.dtos.gateway import UploadFile
# from pdfplumber import pdfplumber

class OCRService:
        
    @staticmethod
    def resize_image(
        image: Image.Image, 
        max_pixels: int = 150000000
    ) -> Image.Image:
        width, height = image.size
        if width * height > max_pixels:
            ratio = (max_pixels / (width * height)) ** 2
            new_size = (int(width * ratio), int(height * ratio))
            image.save(f"resized_{width}_{height}.jpg")
            return image.resize(new_size, Image.Resampling.LANCZOS)
        return image
    
    
    @classmethod
    async def process_ocr_file(
        self,
        pdf_bytes: bytes
    ) -> tuple[list[str], list[str]]:
        # is_pdf = await self.is_pdf_type(file)
        # pdf_bytes = await file.read()
        pages = convert_from_bytes(pdf_bytes)
        page_texts = []
        images = []
        for page in pages:
            image = self.resize_image(page)
            reader = easyocr.Reader(['fr'], gpu=False)
            result = reader.readtext(np.array(image))
            text = " ".join([res[1] for res in result])
            # text = pytesseract.image_to_string(image, config='--psm 1')
            goodcollect_wording = GOODCOLLECT_REGEX.search(text)
            address = ADDRESS_REGEX.search(text)
            if goodcollect_wording or address:
                page_texts.append(text)
        return page_texts, images
    
    @staticmethod
    async def process_ocr_text(self, text: str) -> str:
        pass
    
    
    @staticmethod
    async def process_ocr_image(self, image: Image.Image) -> str:
        pass
    
    @staticmethod
    async def process_pdf(self, ) -> str:
        pass
    
    @staticmethod
    async def is_pdf_type(file: UploadFile) -> bool:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():   # si texte non vide
                    return True
        return False