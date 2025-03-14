import google.generativeai as genai

class GenAIException(Exception):
    """GenAI Exception base class"""

class ChatBot:
    CHATBOT_NAME = 'My Gemini AI'

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-1.0-pro-latest')
        self.conversation = None
        self._conversation_history = []
        self.preload_conversation()

    def send_prompt(self, prompt, temperature=0.1):
        if temperature < 0 or temperature > 1:
            raise GenAIException('Temperature must be between 0 and 1')
        if not prompt:
            raise GenAIException('Prompt cannot be empty')

        try:
            response = self.conversation.send_message(
                content=prompt,
                generation_config=self._generation_config(temperature),
            )
            response.resolve()
            return f'{response.text}\n' + '---' * 20
        except Exception as e:
            raise GenAIException(str(e))

    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature=temperature
        )

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }

    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message('From now on, return the output as a JSON object that can be loaded in python file with the key as \'text\'. For example, {"text":"<output goes here>"}'),
                self._construct_message('{"text":"sure, I can return the output as a JSON object with the key as `text`. Here is an example: {"text":"your Output"}."', 'model')
            ]

    def ChatWithModel(self, message):
        response = self.model.generate_content(message)
        return response.text
