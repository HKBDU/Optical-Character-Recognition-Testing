import re
from dateutil import parser

ALIASES = {
 "certificateNumber": ["certificate no", "certificate number", "certificate id", "cert no"],
 "documentNumber": ["document no", "document number"],
 "horseName": ["horse name", "name of horse"],
 "microchipNumber": ["microchip number", "microchip no", "microchip"],
 "passportNumber": ["passport number", "passport no"],
 "issueDate": ["issue date", "issued date", "date of issue"],
 "expiryDate": ["valid until", "expiry date", "expiration date", "date of expiry"],
 "issuingAuthority": ["issuing authority", "issued by", "competent authority"],
 "originCountry": ["origin country", "country of origin"],
 "destinationCountry": ["destination country", "country of destination"],
 "ownerName": ["owner name", "owner"],
 "veterinarianName": ["veterinarian", "veterinary surgeon"],
 "vaccinationDate": ["vaccination date", "date vaccinated"],
 "vaccineName": ["vaccine name", "vaccine"],
 "invoiceNumber": ["invoice number", "invoice no"],
 "invoiceDate": ["invoice date"],
 "shipmentReference": ["shipment reference", "shipment ref"],
}

def normalize_date(value: str) -> str | None:
    if re.match(r"^\d{1,2}[/-]\d{1,2}[/-]\d{4}$", value.strip()):
        a, b, y = re.split(r"[/-]", value.strip())
        if int(a) <= 12 and int(b) <= 12:
            return None
    try:
        return parser.parse(value, dayfirst=True, fuzzy=False).date().isoformat()
    except (ValueError, OverflowError):
        return None

