from educhain import Educhain, LLMConfig
from langchain_ollama import OllamaLLM

ollama_model = OllamaLLM(model="gemma:2b")
config = LLMConfig(custom_model=ollama_model)

client = Educhain(config)

def generate_mcqs(topic, count=5, question_type="Multiple Choice", difficulty="Medium"):
    questions = client.qna_engine.generate_questions(
        topic=topic,
        num=count,
        question_type=question_type,
        custom_instructions="Include detailed explanations",
        difficulty_level=difficulty
    )
    return questions.model_dump()

def generate_lesson_plan(subject):
    plan = client.content_engine.generate_lesson_plan(topic=subject)
    return plan.model_dump()

def generate_flashcards(topic, count=5):
    flashcards = client.content_engine.generate_flashcards(topic=topic, num=count)
    return flashcards.model_dump()