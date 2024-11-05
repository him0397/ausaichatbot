import logging

from fastapi import APIRouter, HTTPException, Request
from openai import OpenAIError
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.prompt_obs_linking import template
from app.schemas import (
    AutoCompleteRequest,
    AutoCompleteResponse,
    QueryRequest,
    QueryResponse,
)
from app.utilis.openai_client import generate_response

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Configure logging
logger = logging.getLogger("uvicorn.error")


@router.post("/generate-response/", response_model=QueryResponse)
@limiter.limit("10/minute")  # Example rate limit: 5 requests per minute per IP
async def generate_response_endpoint(request: Request, query: QueryRequest):
    try:
        type = "generate_response"
        # Construct the prompt to ensure Australian accent and ACECQA guidelines
        response_prompt = (
            f"Please respond with an Australian tone and accent, ensuring the response aligns with the "
            f"Australian Children's Education and Care Quality Authority (ACECQA) guidelines. "
            f"Your task is to respond to the user query, which is a title based on children's daily care tasks in kindergarten and pre-school. "
            f"The relevant field is: {query.field}. The user query for this field is: {query.query}. Keep the response professional and focused on child education and care quality in Australia."
            f"Provide the response in 5 points. Only points are contain in response "
            f"1.\n2.\n3.\n4.\n5.\n"
        )

        # Call OpenAI API
        response_text = await generate_response(response_prompt, type)

        return QueryResponse(response=response_text)

    except OpenAIError as e:
        logger.error(f"OpenAI API request failed: {e}")
        raise HTTPException(
            status_code=502, detail="Failed to communicate with OpenAI API."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")


@router.post("/autocomplete-template/", response_model=AutoCompleteResponse)
@limiter.limit("10/minute")  # Example rate limit: 5 requests per minute per IP
async def autocomplete_template_endpoint(
    request: Request, template_request: AutoCompleteRequest
):
    try:
        print(template_request.template)
        type = "auto_complete"
        # Construct the prompt for auto-completion
        auto_complete_prompt = (
            f"Please respond with an Australian tone and accent, ensuring the response aligns with the "
            f"Australian Children's Education and Care Quality Authority (ACECQA) guidelines. "
            f"Your task is to improve, expand and sound professional by modify the given template, which is a based on children's daily care tasks in kindergarten and pre-school. "
            f" There are approx. 10 types of observation and linking requirements. Here it is: \n{template}\n\n"
            f"You are given a template with specific fields to be completed. Your task is to fill in these fields based on provided context and relevant details. "
            f"Ensure that each field is completed in a coherent and contextually appropriate manner. "
            f"The provided json template is as follows:\n{template_request.template}\n"
        )

        # Call OpenAI API
        completed_template = await generate_response(auto_complete_prompt, type)

        return AutoCompleteResponse(completed_template=completed_template)

    except OpenAIError as e:
        logger.error(f"OpenAI API request failed: {e}")
        raise HTTPException(
            status_code=502, detail="Failed to communicate with OpenAI API."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
