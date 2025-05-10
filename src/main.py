from src.chains.report_chain import create_report_chain
from src.state.conversation_state import ConversationState
from src.state.state_persistence import save_state, load_state
from src.utils.input_validator import validate_non_empty_string, validate_age
from src.utils.logger import logger

TRIGGER_KEYWORDS = {"new case", "start new patient file", "log new patient"}
QUESTIONS = [
    "What is the patient's name?",
    "What is the patient's age?",
    "What is the patient's primary complaint and its duration?",
    "What are the key clinical observations or vital signs?",
    "Please provide relevant patient history (conditions, allergies, medications)."
]
STATE_KEYS = ["name", "age", "complaint_duration", "key_findings_vitals", "relevant_history"]

def main():
    state_file = "conversation_state.json"
    conversation_state = ConversationState()
    conversation_state.update(load_state(state_file))
    print("🩺 Medical Assistant Ready. Type 'new case' to start.")

    while True:
        user_input = input("\nDoctor: ").strip().lower()
        if user_input in TRIGGER_KEYWORDS:
            logger.info("New case initiated")
            print("Starting a new case. Let's gather details.")

            responses = {}
            for question, key in zip(QUESTIONS, STATE_KEYS):
                while True:
                    response = input(f"\n{question}\nDoctor: ").strip()
                    if key == "age" and not validate_age(response):
                        print("Invalid age. Please enter a number between 0 and 120.")
                        continue
                    if validate_non_empty_string(response):
                        responses[key] = response
                        conversation_state.set(key, response)
                        logger.info(f"Stored {key}: {response}")
                        break
                    print("Invalid input. Please provide a non-empty response.")

            save_state(conversation_state.state, state_file)
            print("\nThank you. Recorded details:")
            for key, value in responses.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

            print("\nGenerating preliminary report...")
            try:
                chain = create_report_chain()
                report = chain.invoke(responses)
                print("\n📝 Preliminary Case Report:")
                print("-" * 50)
                print(report)
                print("-" * 50)
                logger.info("Report generated successfully")
            except Exception as e:
                logger.error(f"Failed to generate report: {e}")
                print("Error generating report.")

            next_step = input("\nStart another case? (yes/no)\nDoctor: ").strip().lower()
            if next_step not in {"yes", "y"}:
                print("Closing session. Take care!")
                break
        elif user_input in {"exit", "quit"}:
            print("Session ended. Goodbye!")
            break
        else:
            print("Unrecognized command. Type 'new case' to begin or 'exit' to quit.")

if __name__ == "__main__":
    main()