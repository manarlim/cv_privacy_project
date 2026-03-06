import fitz
#bech n5rj text mel pdf
doc = fitz.open("cv.pdf")

for page in doc:
    text = page.get_text()
    print(text)
