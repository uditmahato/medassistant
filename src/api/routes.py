from flask import request, jsonify, render_template, send_file
from src.chains.report_chain import create_report_chain
from src.utils.logger import logger
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime

QUESTIONS = [
    "What is the patient's name?",
    "What is the patient's age?",
    "What is the patient's primary complaint and its duration?",
    "What are the key clinical observations or vital signs?",
    "Please provide relevant patient history (conditions, allergies, medications)."
]

def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/get_question", methods=["POST"])
    def get_question():
        data = request.get_json()
        step = data.get("step", 0)
        if step < len(QUESTIONS):
            return jsonify({"done": False, "question": QUESTIONS[step]})
        return jsonify({"done": True})

    @app.route("/generate_report", methods=["POST"])
    def generate_report():
        try:
            data = request.get_json()
            answers = data.get("answers", {})
            report_input = {
                "name": answers.get("name", "Unknown"),
                "age": answers.get("age", "Unknown"),
                "complaint_duration": answers.get("complaint_duration", "Not provided"),
                "key_findings_vitals": answers.get("key_findings_vitals", "Not provided"),
                "relevant_history": answers.get("relevant_history", "Not provided"),
                "current_date": datetime.now().strftime("%Y-%m-%d")
            }
            chain = create_report_chain()
            report_html = chain.invoke(report_input)
            logger.info(f"Generated report: {report_html[:200]}...")
            return jsonify({"success": True, "report": report_html})
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return jsonify({"success": False, "error": str(e)})

    @app.route("/download_pdf", methods=["POST"])
    def download_pdf():
        try:
            data = request.get_json()
            html_content = data.get("html", "")
            if not html_content:
                logger.error("No HTML content provided for PDF")
                return jsonify({"success": False, "error": "No HTML content provided"}), 400

            # Wrap HTML with enhanced styling for OPD PDF
            html_with_styles = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; font-size: 12pt; color: #000; margin: 0.5in; }}
                    h2 {{ font-size: 16pt; font-weight: bold; margin: 10px 0; text-align: center; }}
                    h3 {{ font-size: 14pt; font-weight: bold; margin: 8px 0; }}
                    p {{ margin: 5px 0; line-height: 1.4; }}
                    ul {{ list-style-type: disc; padding-left: 20px; margin: 10px 0; }}
                    li {{ margin-bottom: 5px; }}
                    hr {{ border: 0; border-top: 1px solid #000; margin: 15px 0; }}
                    strong {{ font-weight: bold; }}
                    .header {{ text-align: center; margin-bottom: 20px; }}
                    .disclaimer {{ font-style: italic; font-size: 10pt; margin-top: 20px; }}
                    .notes {{ margin-top: 10px; font-size: 10pt; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>Outpatient Department (OPD) Report</h2>
                    <p><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>
                </div>
                {html_content}
            </body>
            </html>
            """

            # Generate PDF
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html_with_styles, dest=pdf_buffer)
            if pisa_status.err:
                logger.error(f"PDF generation failed: {pisa_status.err}")
                return jsonify({"success": False, "error": "PDF generation failed"}), 500

            pdf_buffer.seek(0)
            logger.info("PDF generated successfully")
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='opd_medical_report.pdf'
            )
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return jsonify({"success": False, "error": str(e)}), 500