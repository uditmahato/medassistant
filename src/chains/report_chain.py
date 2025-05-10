from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from src.llm.gemini_provider import get_gemini_llm
from src.chains.prompts.report_prompt import REPORT_PROMPT
from src.utils.logger import logger

def clean_output(output: str) -> str:
    """Remove unwanted backticks or markdown code block markers from the output."""
    cleaned = output.strip()
    if cleaned.startswith("```html") or cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1].rsplit("\n", 1)[0]
    return cleaned.strip()

def create_report_chain(model_name="gemini-1.5-flash", temperature=0.0):
    try:
        llm = get_gemini_llm(model_name=model_name, temperature=temperature)
        prompt = PromptTemplate.from_template(REPORT_PROMPT)
        chain = prompt | llm | StrOutputParser() | clean_output
        logger.info("Report chain created successfully")
        return chain
    except Exception as e:
        logger.error(f"Error creating report chain: {e}")
        raise