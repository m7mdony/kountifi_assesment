# PDF Invoice Parser

This project uses the Gemini Agent Framework to extract and parse data from PDF invoices. It uses the Gemini AI model to intelligently extract structured data from invoice PDFs.

## Prerequisites

- Python 3.8 or higher
- Google Cloud account with Gemini API access
- PDF invoice file to process

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root directory with your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

To get a Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and paste it in your `.env` file

## Usage

1. Place your PDF invoice file in the project directory
2. Update the `invoice_path` variable in `parse.py` to match your PDF filename
3. Run the script:
```bash
python parse.py
```

The script will:
1. Extract text from the PDF invoice
2. Parse the extracted text to identify key invoice information
3. Store the structured data in a JSON file named `invoice_data.json`

## Output

The script generates an `invoice_data.json` file containing the parsed invoice data in a structured format. The JSON file includes:
- Invoice title
- Invoice number
- Invoicer details
- Date
- Total amount
- Items in the invoice
- Any other relevant details found in the invoice

## Error Handling

The script includes error handling for:
- Missing PDF file
- Invalid PDF format
- API key issues
- JSON parsing errors

If any errors occur, they will be displayed in the console output.

## Notes

- Make sure your PDF is text-based (not scanned images)
- The Gemini API key should be kept secure and never committed to version control
- The script uses the `gemini-1.5-flash` model by default
