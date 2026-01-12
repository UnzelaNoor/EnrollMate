# EnrollMate – AI Admission Assistant

EnrollMate is an AI-powered admission chatbot built using **Flask**, **OpenAI API**, and a custom-designed frontend.  
It is designed to answer **only admission-related queries** for NovaTech University using structured data from a JSON file.

The chatbot behaves like a real admission officer:
- Answers questions about eligibility, programs, fees, process, etc.
- Uses only the data provided in `data.json`
- Refuses out-of-scope questions politely
- Never hallucinates or assumes missing information

---

## 🚀 Features

- Admission-focused AI assistant  
- Data-driven responses using `data.json`  
- No hallucination – answers strictly from provided data  
- Polite refusal for out-of-scope queries  
- Clean chat-style UI  
- Frontend (HTML/CSS/JS) + Flask backend  
- OpenAI GPT integration  

---

## 🛠 Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **AI:** OpenAI API  
- **Data Source:** JSON file  
- **Environment:** Python Virtual Environment  

---

## 📂 Project Structure
EnrollMate/
│
├── app.py
├── requirements.txt
├── .gitignore
├── data/
│ └── data.json
├── templates/
│ └── index.html
└── static/
├── style.css
└── script.js


---

## ⚙️ Setup & Run

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# or
source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your API key
# .env
OPENAI_API_KEY=your_openai_key_here

# Run the app
python app.py
