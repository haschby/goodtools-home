import re

GOODCOLLECT_VALUE = r"GOODCOLLECT|GOOD COLLECT"
EXCLUDING_WORDS = ["PESEE",]

GOODCOLLECT_REGEX = re.compile(GOODCOLLECT_VALUE, re.IGNORECASE)
ADDRESS_REGEX = re.compile(r"28 (?:BD|Boulevard) GEORGES CLEMENCEAU\s*13200 Arles")
GC_BOOKING_REGEX = re.compile(r"GC\s*[-]?\s*\d+")
AMOUNT_REGEX = re.compile(r'\d{1,3}(?:[ .\u00A0]?\d{3})*(?:[.,]\d+)\s*€?')
#\d{1,3}(?:[ .\u00A0]?\d{3})*(?:[.,]\d+)\s*€?
AMOUNT_REGEX_WITH_SYMBOL = re.compile(r'(?:\d{1,3}(?:[ \.\u00A0]\d{3})*(?:[.,]\d+)|\d+(?:[.,]\d+)?)\s*€')

TVA_NUMBER_REGEX = re.compile(r'^(FR|BE|ES|DE|IT|NL|AT|PT|LU|CH|GB)\d{11}$')

FACTURE_REGEX = re.compile(r'FACTURE TICKET') # TO BE DEFINED


TVA_REGEX = re.compile(
    r'(?:\b\d{1,2}(?:[.,]\d+)?\s*%\s*€?|Total\s*TVA\s*\d+(?:[.,]\d+)?)',
    re.IGNORECASE
)
ONLY_FLOAT_REGEX = re.compile(r'\d+(?:[.,]\d+)?')

def extract_float(text) -> float:
    if not text:
        return 0
    
    if type(text) == str:
        
        match = re.compile(r'\d+(?:[.,]\d+)?').search(text.replace(" ", ""))
        if match:
            number_str = match.group(0).replace(" ", "").replace(",", ".")
            return float(number_str)
    
    float_match = re.compile(r'\d+(?:[.,]\d+)?').search(text.group(0))
    if float_match:
        return float(float_match.group(0))
    return 0