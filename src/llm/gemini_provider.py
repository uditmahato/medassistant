from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import get_google_api_key
from src.utils.logger import logger

def get_gemini_llm(model_name="gemini-1.5-flash", temperature=0.0):
    try:
        api_key = get_google_api_key()
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature
        )
        logger.info(f"Gemini LLM initialized with model {model_name}")
        return llm
    except Exception as e:
        logger.error(f"Error initializing Gemini LLM: {e}")
        raise