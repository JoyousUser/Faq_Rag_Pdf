from django.db import models
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain.output_parsers import PydanticOutputParser 
from pydantic import BaseModel, Field
import PyPDF2, json, re

class FAQGenerator:
    model_name = 'llama3'
    class FAQ(BaseModel):
            question: str = Field(description='FAQ question')
            answer: str = Field(description='FAQ réponse')

            model_config = {
                "from_attributes": True
            }
    output_parser = PydanticOutputParser(pydantic_object=FAQ)
    ai_prompt = PromptTemplate(
    template=(
               """
                Tu es une IA qui NE PARLE QU’EN FRANÇAIS et qui EXTRAYE uniquement des FAQ d’un texte fourni.

                Voici ce que tu dois faire :
                - Lis le texte ci-dessous.
                - Génère exactement 10 objets JSON représentant des FAQ.
                - Chaque objet doit avoir cette structure (et rien d'autre) :

                {format_instructions}

                TRÈS IMPORTANT : Tu dois renvoyer UNIQUEMENT un tableau JSON brut de 10 objets (pas de texte, pas de phrase, pas d’explication).

                Voici le texte d’entrée :

                <<<
                {text}
                >>>

                ENVOIE LE RESULTAT SANS COMMENTAIRE, NI ESPACE, NI INTRODUCTION
                """
        ),
        input_variables=["text"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()},
    )

    @property
    def ai_model(self):
        return self.model_name
    
    @ai_model.setter
    def ai_model(self, model_name):
        self.model_name = model_name
    

    def generate_ai_prompt(self, uploaded_file):
        llm = Ollama(model=self.model_name, timeout=120)
        print('Request recieved')
        def extract_text_from_pdf(uploaded_file):
            with open(uploaded_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        
        
        def repair_and_parse_json_array(output: str):
            print('Attempting to repair and parse json array')
            # Find all JSON objects individually
            objects = re.findall(r'\{\s*"question"\s*:\s*".+?",\s*"answer"\s*:\s*".+?"\s*\}', output, re.DOTALL)

            if not objects:
                raise ValueError("No valid FAQ JSON objects found.")

            # Reconstruct a proper JSON array
            json_array_str = "[\n" + ",\n".join(objects) + "\n]"

            try:
                return json.loads(json_array_str)
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON failed to parse after repairing json array: {e}")
            
        # Main AI out generator
        pdf_text = extract_text_from_pdf(uploaded_file)
        response = None
        try:
            print('Generating...')
            sequence = self.ai_prompt | llm
            response = sequence.invoke({"text": pdf_text})
            response = json.loads(response)
        except Exception as e:
            print("Error during AI prompt generation: ", e)
            # response = repair_and_parse_json_array(response)

        if response:
            return response

        print('Error getting AI response!')        