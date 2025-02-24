import unittest
from unsloth import convert_to_conversation, FastLanguageModel, formatting_prompts_func  # Replace 'your_module' with the actual module name

def test_model_loading(): # Ensures the model and tokenizer load without issues.
    model_name = "unsloth/Llama-3.2-3B-Instruct"
    model, tokenizer = FastLanguageModel.from_pretrained(model_name)
    assert model is not None, "Model failed to load"
    assert tokenizer is not None, "Tokenizer failed to load"

class TestFineTuneFunctions(unittest.TestCase): # esures that we produce correctly structured training data.
    def test_convert_to_conversation(self):
        sample_input = {
            "instruction": "Follow this guideline.",
            "input": "Fever, cough, sore throat",
            "output": "Possible flu."
        }
        expected_output = {
            "conversations": [
                {"from": "system", "value": "Follow this guideline."},
                {"from": "human", "value": "Predict the disease based on these symptoms: Fever, cough, sore throat"},
                {"from": "gpt", "value": "Possible flu."}
            ]
        }
        self.assertEqual(convert_to_conversation(sample_input), expected_output)
    
    def test_formatting_prompts(self): # test helps catch formatting errors if not the fine-tuning process could break
        tokenizer = FastLanguageModel.from_pretrained("unsloth/Llama-3.2-3B-Instruct")[1]
        example_convo = {"conversations": [{"from": "human", "value": "Hello!"}]}
        formatted = formatting_prompts_func({"conversations": [example_convo]})
        self.assertIn("text", formatted, "Formatting function should return a text key")

if __name__ == "__main__":
    test_model_loading()
    unittest.main()
