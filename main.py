"""Testing module for shared_python"""

from shared_open_ai.chat import OpenAIChat

ai_test = OpenAIChat()

response = ai_test.send_message("What is the difference between interpeted langauge and compiled langauge?")
print(response)

response2 = ai_test.send_message("Great, which of those is python?")
print(response2)
