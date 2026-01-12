from flask import Flask, request, jsonify, render_template  
from openai import OpenAI 
import json    
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an admission assistant chatbot for NovaTech University. Your role is to assist prospective and current students by answering questions related to university admissions.
You must answer only admission-related queries, including but not limited to eligibility criteria, fee structure, available programs, admission process, and important dates. You must not answer questions that are unrelated to admissions, even if they are related to the university.
The official admission data will be provided below. This data is the only source of truth for your answers. You must use only the provided data to answer student queries and must not rely on external knowledge or assumptions.
If the requested information is not explicitly available in the provided data, clearly state that you do not have that information. Do not attempt to infer, guess, or generate information that is not present.
If a question is out of scope, politely respond that you can only assist with admission-related queries and ask the user to rephrase their question accordingly.
All responses should be clear, concise, and to the point. Maintain a professional yet student-friendly tone. Do not include emojis, markdown tables, or unnecessary additional information.
"""

INTENT_MAP = { 
    "university" : "University_Name",
    "eligibility": "Eligibility",
    "fee": "Fee_Structure",
    "fees": "Fee_Structure",
    "program": "Programs_Offered",
    "admission process": "Admission_Process",
    "document": "Required_Documents",
    "scholarship": "Scholarships_Financial_Aid",
    "entry test": "EntryTest_Details",  
    "international students": "International_Students", 
    "contact information" : "Contact_Information"
} 
SUB_INTENT_SECTIONS = {
    "Programs_Offered": {
        "bs": ["bs", "undergraduate", "bachelor"],
        "ms": ["ms", "postgraduate", "master"]
    },
    "Eligibility": {
        "undergraduate": ["undergraduate", "undergrad", "bs"],
        "postgraduate": ["postgraduate", "ms"]
    },
    "Fee_Structure": {
        "undergraduate_programs": ["undergraduate", "bs"],
        "graduate_programs": ["postgraduate", "ms"]
    },
    "Scholarships_Financial_Aid": {
        "bs": ["bs", "undergraduate"],
        "ms": ["ms", "postgraduate"]
    }
}


app =Flask(__name__) 
with open("data/data.json", "r", encoding ="utf-8") as file: 
    admission_data= json.load(file) 

def format_admission_data(data): 
    return json.dumps(data, indent=2)   

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods= ["POST"]) 
def chat(): 
    data = request.get_json() 
    raw_question = data.get("question", "")  
    question = raw_question.strip().lower()   
    formatted_data= format_admission_data(admission_data) 
    matched = False 
    relevant_data= None 

    for key in INTENT_MAP: 
        if key in question:  
            matched = True
            json_key = INTENT_MAP[key] 
            section_data =admission_data[json_key]  

            if json_key in SUB_INTENT_SECTIONS and isinstance(section_data, dict): 
                sub_map = SUB_INTENT_SECTIONS[json_key] 
                for sub_key, keywords in sub_map.items(): 
                    for word in keywords: 
                        if word in question and sub_key in section_data:
                          relevant_data = section_data[sub_key] 
            else: 
               relevant_data = section_data 

            break
    messages = [ 
        {"role": "system", "content": SYSTEM_PROMPT}, 
        { 
            "role": "system", 
             "content": f"Official admission data:\n{formatted_data}"
        }
    ] 

    if relevant_data: 
        messages.append({ 
            "role": "system", 
             "content": f"Relevant extracted information:\n{relevant_data}"
        }) 

    messages.append({
        "role": "user",
        "content": raw_question
    })  

    # print("\n===== CHAT DEBUG START =====")
    # print("RAW QUESTION:", raw_question)
    # print("MATCHED:", matched)
    # print("RELEVANT DATA:", relevant_data)
    # print("\nMESSAGES SENT TO AI:")
    # for msg in messages:
    #    print(msg)
    # print("===== CHAT DEBUG END =====\n")

    try: 
        response = client.chat.completions.create( 
            model = "gpt-4o-mini", 
            messages = messages, 
            temperature= 0.2
        ) 

        ai_reply =response.choices[0].message.content.strip() 

        return jsonify({ 
            "reply": ai_reply
        }) 
    except Exception as e: 
       return jsonify({ 
            "reply": "Sorry I am having trouble answering right now"
        }) ,500

if __name__ == "__main__": 
    app.run(debug=True)