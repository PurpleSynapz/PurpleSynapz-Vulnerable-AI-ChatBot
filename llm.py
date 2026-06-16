from langchain_ollama import OllamaLLM



def generate_llm_response(prompt, base_url, llm_model):
    try:
        print(f"[LLM] Model: {llm_model}")
        print(f"[LLM] Prompt:\n{prompt}\n")
        llm = OllamaLLM(model=llm_model, base_url=base_url, temperature=0.7)


        response = llm.invoke(prompt)
        print(f"[LLM] Response:\n{response}\n")

        if hasattr(response, "content"):
            return response.content

        return response

    except Exception as e:
        print(f"[LLM] Error: {str(e)}")
        return f"Error: {str(e)}"


def Classify_llm_response(prompt, base_url, llm_model):
    try:
        print(f"[LLM] Model: {llm_model}")
        print(f"[LLM] Prompt:\n{prompt}\n")
        llm = OllamaLLM(model=llm_model, base_url=base_url, **{
            "temperature": 0,
            "response_format": {
                "type": "json_object"
            }
        })

        response = llm.invoke(prompt)
        print(f"[LLM] Response:\n{response}\n")

        if hasattr(response, "content"):
            return response.content

        return response

    except Exception as e:
        print(f"[LLM] Error: {str(e)}")
        return f"Error: {str(e)}"