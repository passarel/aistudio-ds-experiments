from framework_classes.prompt import Prompt
from framework_classes.prompt_template import PromptTemplate
from framework_classes.vectordb import VectorDB
from framework_classes.message import Message
from framework_classes.memory import Memory

class DemoPrompt(Prompt):
    """
        Specialization of a `Prompt`.\n
        Functions:
            - get_prompt(): apply the given inputs to a template.
    """

    def __init__(self, template: PromptTemplate, db: VectorDB) -> None:
        """Creates an instance with a specified template and VectorDB."""
        self.template = template
        self.db = db
    
    def get_prompt(self, message: Message, history: Memory) -> str:
        """
            Apply the given inputs to the template.\n
            Parameter:
                A Message object with the user's text string
                and Message history
            Return:
                A text string using the template with the inputs
        """
        # Query the VectorDB with the message content and get background information
        background = self.db.query(message.content)
        
        # Apply the template with the provided inputs (message, history, background)
        # and ensure that the function returns only the string result of the template application
        prompt_text = self.template.apply(message=message, history=history, background=background)
        
        # Return the final prompt text as a string
        return prompt_text