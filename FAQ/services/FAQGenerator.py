from django.db import models
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama 
import PyPDF2, json

class FAQGenerator:
    model_name = 'llama3'
    ai_prompt = PromptTemplate(
    template=(
        """You are a french AI assistant that extracts useful FAQs from a given text. Your task is to read the following content and generate a list of frequently asked questions (FAQs) with concise answers. Each FAQ should be a JSON object with the following format:{{"question": "A common or important question based on the text.","answer": "A concise, informative answer drawn from the text."}} Return the result as a JSON array of FAQ objects. Here is the input text: {text} Please return only the JSON array of FAQs, with no explanation or additional commentary."""
        ),
        input_variables=["text"],
    )
    llm = Ollama(model=model_name, timeout=120)

    def generate_ai_prompt(self, uploaded_file):
        print('Request recieved')
        def extract_text_from_pdf(uploaded_file):
            with open(uploaded_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = None
        try:
            print('Generating...')
            sequence = self.ai_prompt | self.llm
            response = sequence.invoke({"text": pdf_text})
            response = response.strip()
            response = json.loads(response)
        except Exception as e:
            print("Error during AI prompt generation:", e)
        
        if response: 
            return response

        print('Error getting AI response')