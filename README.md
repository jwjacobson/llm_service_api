# LLM Service API
The LLM Service API is built using Django and Django REST Framework and provides access to OpenAI, Google Gemini, and our in-house LLM.

## Requirements
- [Python 3.13](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
Note: these instructions will assume you are using uv for project and dependency management. If you use another tool, you will need to modify the provided commands to work with it.
- [OpenAI API key](https://platform.openai.com/api-keys) (to interact with OpenAI LLMs)
- [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) (to interact with Gemini LLMs)

## Installation
1. [Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2. Navigate to the llm_service_api directory
3. Copy the contents of env-template into a file named `.env` in the project's root directory, and fill in appropriate values without quotation marks. This app uses `python-decouple` to manage environment variables, and will not run unless they are set.

## Running the API
To start the server, run `uv run python manage.py runserver`

## Using the endpoints
### In a web browser
The easiest way to try out the endpoints is by using the Django REST Framework's browsable API: just open http://127.0.0.1:8000 (or your local host if the address is different) in a web browser. Enter json into the provided text box to send it to the ednpoint.

### Using curl
If you prefer, you can use curl or another utility to send requests directly from the command line. Here is a sample curl POST request using Google Gemini:


## API endpoints
### Welcome: `GET /`
Returns a welcome message. If you cannot access this, the server is probably not running.
*Curl*
`curl http://127.0.0.1/`

### Signup: `POST /api/signup/`
Create a user.
`curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'`

### Token: `POST /api/token/`
Get an access token to use for protected endpoints and a refresh token to refresh the access token. Username and password must belong to a user you created via the signup endpoint.
`curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "$USERNAME", "password": "$PASSWORD"}'`

### Refresh: `POST /api/token/refresh`
Refresh your access token if it has expired.
`curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "$REFRESH_TOKEN"}'`

### Supported models: `GET /api/supported-models/?provider=$PROVIDER`
Returns a list of the supported models of a given provider. Supported providers are openai, gemini, and inhouse.
`curl http://localhost:8000/api/supported-models/\?provider\=gemini \
  -H "Authorization: Bearer $ACCESS_TOKEN"`

### Chat completion: `POST /api/chat/completions/?provider=$PROVIDER`
Returns a response to a submitted query. Supported providers are openai, gemini, and inhouse.
`curl -X POST 'http://localhost:8000/api/chat/completions/?provider=openai' \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
        "model": "gpt-3.5-turbo",
        "messages": [
          {"role": "user", "content": "How is the weather on Venus?}
        ],
        "stream": false
      }'`
