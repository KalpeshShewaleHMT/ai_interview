from gemini_service import GeminiService

class InterviewEngine:
    def __init__(self, topic, difficulty, total_questions):
        self.topic = topic
        self.difficulty = difficulty
        self.total_questions = total_questions
        self.gemini = GeminiService()

    def build_prompt(self, history, question_number):
        if question_number == self.total_questions:
            return f"""
You are a professional technical interviewer.

Based on the entire conversation below:

1. Give overall feedback.
2. Give a score out of 10.
3. Format strictly as:

FEEDBACK:
<feedback text>

SCORE:
<number>

Conversation:
{history}
"""

        return f"""
You are a professional technical interviewer.
Topic: {self.topic}
Difficulty: {self.difficulty}

Ask question number {question_number} only.
Ask ONE question.
Do not explain answers.
Do not provide feedback yet.
Conversation so far:
{history}
"""

    def next_question(self, history, question_number):
        prompt = self.build_prompt(history, question_number)
        return self.gemini.generate(prompt)
