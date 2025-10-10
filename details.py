import requests

url = "https://www.sec.gov/Archives/edgar/data/320193/000130817925000008/aapl4359751-def14a.htm"
headers = {"User-Agent": "yourname@example.com"}
html = requests.get(url, headers=headers).text
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")
text = soup.get_text(" ", strip=True)
import textwrap

chunks = textwrap.wrap(text, 3000)  # approx 3000 chars per chunk
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt_template = """
You are a financial data extractor. From the following SEC filing text, extract the following fields in JSON format:

Entity Metadata:
- registered_legal_name
- country_of_incorporation
- registered_business_address
- company_identifiers (CIK, IRS number, SEC file number)

Principals:
- full_name
- position
- ownership_percentage

Company Profile:
- description
- number_of_employees
- annual_revenue
- website_url

Text:
"""

# Use first chunk for example
response = pipe(prompt_template + chunks[0], max_new_tokens=500)
print(response[0]["generated_text"])
