import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import json
from . import rag_logic

# Load environment variables
load_dotenv()

def chat_view(request):
    """
    Renders the main chat interface page.
    """
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def ask_question(request):
    """
    An API endpoint to handle user questions and return the chatbot's answer.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get('question')
        if not question:
            return JsonResponse({'error': 'No question provided'}, status=400)

        # --- RAG Logic Integration ---
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return JsonResponse({'error': 'Google API Key not configured on the server.'}, status=500)

        # 1. Get Text Content
        text_content = rag_logic.get_text_content()
        if not text_content:
            return JsonResponse({'error': 'Could not load the biography knowledge base.'}, status=500)

        # 2. Build Vector Store (uses cache)
        vector_store = rag_logic.build_vector_store(text_content, api_key)
        if not vector_store:
            return JsonResponse({'error': 'Failed to build the vector store.'}, status=500)

        # 3. Create RAG Chain and Invoke
        rag_chain = rag_logic.get_rag_chain(vector_store, api_key)
        if not rag_chain:
            return JsonResponse({'error': 'Failed to create the RAG chain.'}, status=500)

        response = rag_chain.invoke({"input": question})
        answer = response.get('answer', "Sorry, I couldn't find an answer to that.")

        return JsonResponse({'answer': answer})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred in ask_question view: {e}")
        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)
