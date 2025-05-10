# Medical Chat Assistant

A Flask-based web application that collects patient information via a chat interface and generates preliminary medical reports using Google Gemini LLM. The app refines patient complaints into clinical terminology, provides specific clinical recommendations (prescriptions, diagnoses, treatments), and exports reports as PDFs. The UI features a modern chat design with dark mode, toast notifications, and Tailwind CSS styling.

## Features

* **Chat Interface** : Collects patient data (Name, Age, Complaint & Duration, Vitals, History) via static questions in a conversational UI.
* **LLM-Powered Reports** : Google Gemini refines complaints (e.g., "ABDOMEN PAIN" → "Acute lower right abdominal pain") and generates doctor-like recommendations for prescriptions (Rx), differential diagnoses (Dx), treatments (Tx), and case management.
* **Report Format** : Structured HTML reports with `prose-medical` styling, including emojis (🩺, ⚠️) for on-screen display.
* **PDF Export** : Generates downloadable PDFs using `xhtml2pdf`, with emojis replaced for compatibility (e.g., 🩺 → "[Stethoscope]").
* **UI Enhancements** : Dark mode toggle, toast notifications, custom scrollbars, and typing indicators.
* **Safety** : Emphasizes preliminary guidance, requiring physician review for final decisions.

## Prerequisites

* **Python** : 3.8 or higher
* **Google Gemini API Key** : Obtain from Google Cloud Console
* **Dependencies** : Listed in `requirements.txt`

## Setup

1. **Clone the Repository** :

```bash
   git clone <repository-url>
   cd medical-chat-assistant
```

1. **Create a Virtual Environment** :

```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. **Install Dependencies** :

```bash
   pip install -r requirements.txt
```

1. **Set Environment Variables** :

```bash
   export GOOGLE_API_KEY="your-google-gemini-api-key"
```

   On Windows:

```cmd
   set GOOGLE_API_KEY=your-google-gemini-api-key
```

1. **Run the Application** :

```bash
   python -m src.api.app
```

   Access the app at `http://localhost:5000`.

## Usage

1. **Start a New Case** :

* Open `http://localhost:5000` in a browser.
* Type `New case` in the chat input to begin.
* Answer the static questions:
  * What is the patient's name?
  * What is the patient's age?
  * What is the patient's primary complaint and its duration?
  * What are the key clinical observations or vital signs?
  * Please provide relevant patient history (conditions, allergies, medications).

1. **Generate Report** :

* After answering all questions, the app generates a medical report displayed in the chat with `prose-medical` styling.
* Example report for inputs (Name: UDIT, Age: 28, Complaint: ABDOMEN PAIN for 3 days, Vitals: BP 120/80, sharp pain in lower right abdomen, History: No allergies, mild nausea):
  ```
  🩺 Preliminary Medical Report
  Disclaimer: This AI-generated report is for preliminary guidance only...
  1. Patient Summary
    - Patient Name: UDIT
    - Patient Age: 28
    - Chief Complaint: Acute lower right abdominal pain for 3 days
    - Key Clinical Findings: BP 120/80, sharp pain in lower right abdomen
    - Relevant History: No allergies, mild nausea
  2. Rx – Potential Prescription Considerations
    - Ranitidine 150 mg twice daily for suspected gastric irritation.
    - Avoid NSAIDs to prevent exacerbation of potential gastric issues.
  3. Dx – Potential Differential Diagnoses
    - Acute appendicitis, rule out gastritis.
    - Confirm with clinical evaluation and diagnostic tests.
  4. Tx – Potential Treatment Strategies
    - Abdominal ultrasound to evaluate appendix and abdominal organs.
    - Monitor response and adjust plan as needed.
  5. Case Management Steps
    - History: No allergies, safe for standard medications.
    - Investigations: Order abdominal ultrasound and complete blood count.
    - Consultations: Refer to gastroenterologist for persistent symptoms.
    - Patient Education: Discuss potential causes of abdominal pain and importance of imaging.
  ⚠️ Note: This is a preliminary interpretation...
  ```

1. **Download PDF** :

* Click the download button (green, with 📥 icon) to export the report as `medical_report.pdf`.
* Emojis are replaced (e.g., 🩺 → "[Stethoscope]") for PDF compatibility.

1. **Dark Mode** :

* Toggle dark mode using the moon/sun icon in the navbar.

## Project Structure

```
medical-chat-assistant/
├── logs/
│   └── app.log              # Application logs
├── src/
│   ├── api/
│   │   ├── app.py          # Flask app configuration
│   │   └── routes.py       # API endpoints (/get_question, /generate_report, /download_pdf)
│   ├── chains/
│   │   ├── prompts/
│   │   │   └── report_prompt.py  # LLM prompt for report generation
│   │   └── report_chain.py       # LangChain setup for LLM
│   ├── templates/
│   │   └── index.html       # Frontend UI (chat interface)
│   └── utils/
│       └── logger.py        # Logging configuration
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Files Description

* **`src/api/app.py`** : Initializes the Flask app and registers routes.
* **`src/api/routes.py`** : Defines endpoints for fetching questions, generating reports, and downloading PDFs.
* **`src/chains/prompts/report_prompt.py`** : Configures the LLM prompt to refine complaints and generate specific clinical recommendations.
* **`src/chains/report_chain.py`** : Sets up LangChain to invoke the Google Gemini LLM.
* **`src/templates/index.html`** : Renders the chat UI with Tailwind CSS, Axios for API calls, and Font Awesome icons.
* **`requirements.txt`** : Lists dependencies (e.g., `flask`, `xhtml2pdf`, `langchain`, `google-generativeai`).

## Dependencies

Key dependencies (see `requirements.txt` for full list):

* `flask`: Web framework
* `xhtml2pdf`: PDF generation
* `langchain`: LLM integration
* `google-generativeai`: Google Gemini API
* `axios`: Frontend HTTP requests (CDN)
* `tailwindcss`: Styling (CDN)
* `font-awesome`: Icons (CDN)

## Customization

* **LLM Tone** : The LLM is configured for professional, doctor-like recommendations (e.g., "Ranitidine 150 mg twice daily"). For a playful tone (e.g., "Take two aspirin and call me in the morning"), modify `report_prompt.py` by adjusting the prompt instructions to allow informal language, but ensure clinical accuracy.
* **Report Styling** : Edit `prose-medical` CSS in `index.html` or the HTML template in `report_prompt.py`.
* **Clinic Branding** : Update "Medical Chat Assistant" in `index.html` or add a clinic name in `routes.py` (PDF header).
* **Questions** : Modify the `QUESTIONS` list in `routes.py` to change input fields.

## Troubleshooting

1. **LLM Neutral Outputs** :

* Check `GOOGLE_API_KEY` is set.
* Inspect `logs/app.log` for LLM errors.
* Test LLM output by logging in `report_chain.py`:
  ```python
  test_input = {"name": "UDIT", "age": "28", "complaint_duration": "ABDOMEN PAIN for 3 days", ...}
  logger.info(chain.invoke(test_input))
  ```

1. **PDF Issues** :

* If emojis render as boxes, verify `routes.py` replaces them (`[Stethoscope]`, `[Warning]`).
* Check `logs/app.log` for `xhtml2pdf` errors.

1. **UI Errors** :

* Open browser Developer Tools (F12) → Console/Network.
* Verify `/get_question`, `/generate_report`, `/download_pdf` responses.
* Share console logs or response errors.

1. **Report Format** :

* Inspect `report-content` HTML in the chat container.
* Ensure `prose-medical` class is applied.

## Notes

* **LLM Role** : The LLM refines complaints and provides specific recommendations, acting as a doctor while emphasizing physician review.
* **PDF Compatibility** : Emojis are replaced for `xhtml2pdf`. For emoji support, consider `WeasyPrint` (requires dependency changes).
* **Production** : Monitor Gemini API quotas and ensure `xhtml2pdf` dependencies are installed.
* **Playful Tone** : To add comically specific recommendations (e.g., "Take two aspirin and call me in the morning"), update `report_prompt.py` with a conditional tone switch, but maintain clinical accuracy for safety.

## License

MIT License. See [MIT License](LICENSE) file for details.

## Contact

For issues or feature requests, open a GitHub issue or contact the maintainer.
