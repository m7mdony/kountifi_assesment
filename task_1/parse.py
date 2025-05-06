import json

from gemini_agent import Agent #this is the framework that is submmitted in task 11 to showcase its capabilities
import os
import pdfplumber

from dotenv import load_dotenv

load_dotenv()




def convert_to_json(data: str):
    return json.loads(data)

#define the tool to store the data as a JSON file
@Agent.description("This tool is used to store the data as a JSON file")
@Agent.parameters({
    "file_path": {"type": "string", "description": "The path to the file to store the data"},
    "data": {"type": "object", "description": "a json data to be stroed in a json file"}
    })
def store_data(file_path: str, data: dict):
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(json.loads(data), f, indent=4, ensure_ascii=False)
        return "Data stored successfully"
    except Exception as e:
        return f"Error storing data: {e}"




def validate_pdf_path(pdf_path: str):
    # check if the path exsit and if it is a pdf file
    if not os.path.exists(pdf_path):
        raise ValueError("The file does not exist")
    if not pdf_path.endswith(".pdf"):
        raise ValueError("The file is not a PDF file")

@Agent.description("This tool is used to extract the text from the invoice")
@Agent.parameters({
    "pdf_path": {"type": "string", "description": "The path to the PDF file to extract the text from"}
    })
def extract_text_from_pdf(pdf_path: str):
    try:
        print(f"Extracting text from {pdf_path}")
        validate_pdf_path(pdf_path)
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total pages in PDF: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                print(f"Page {i+1} text length: {len(page_text)}")
                text += page_text
        print(f"Total extracted text length: {len(text)}")
        return text
    except Exception as e:
        print(f"Error details: {str(e)}")
        return f"Error extracting text from PDF: {e}"



@Agent.description("This tool is used to read the variable in the agent list of variables")
@Agent.parameters({
    "variable_name": {"type": "string", "description": "The name of the variable to read"}
    })
def read_variable(variable_name: str):
    return agent.get_variable(variable_name)

#initialize the agent
agent = Agent(
    api_key=os.getenv("GEMINI_API_KEY"),
    model_name="gemini-1.5-flash",
    tools=[store_data, extract_text_from_pdf, read_variable],

)


#the path to the invoice
invoice_path = "Kountifi.pdf"


#invisble variable to store the invoice path that will be used by the agent

#this varaible will not take long input token in the prompt so it can be as short or as long as needed
agent.set_variable(
    name="Kountifi invoice path",
    value=invoice_path,
    description="the path to the invoice",
    type_hint=str
)


system_prompt = """
you are a helpful assistant that extracts data from a PDF invoice and stores it in a JSON file.
you will be givent a PDF path and you will need to extract the text using the extract_text_from_pdf tool.
then you will need to parse the information about the invoice and extract all the needed data,
such as the title of the invoice,invoice number, invoicer details, date, total amount, and the items in the invoice, and any other details that is mentioned in the invoice.
the data should be stored in a JSON file using the store_data tool.
"""

user_prompt = "Extract the data from the Kountifi invoice using the extract_text_from_pdf tool then store the data in a JSON file using the store_data tool you can always read the data using the read_variable tool. at the end tell me if you have successfully stored the data in a JSON file."

response = agent.prompt(
    user_prompt=user_prompt,
    system_prompt=system_prompt,
    response_structure={
        "type": "OBJECT",
        "properties": {
            "status": {"type": "STRING", "description": "the status of the data storage"},
        }
    }
)


print(response)



