import fitz # PyMuPDF
doc = fitz.open("/home/duy/cocarry_ws/adaptive_weight/1805.06270v3.pdf")
for page in doc:
    print(page.get_text("text"))
