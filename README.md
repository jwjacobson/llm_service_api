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

The easiest way to try out the endpoints is by using Django REST Framework's browsable API. Just open [http://127.0.0.1:8000](http://127.0.0.1:8000) (or your local host if the address is different) in a web browser. Enter JSON into the provided text box to send it to the endpoint.

### Using curl

If you prefer, you can use `curl` or another utility to send requests directly from the command line. Below are examples of both the request JSON (if applicable) and the corresponding `curl` command.

---

## API endpoints

### Welcome — `GET /`

Returns a welcome message. If you cannot access this, the server is probably not running.

```bash
curl http://127.0.0.1/
```

---

### Signup — `POST /api/signup/`

Creates a user.

**JSON:**
```json
{
  "username": "testuser",
  "password": "testpass"
}
```

**curl:**
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

---

### Token — `POST /api/token/`

Get an access token and a refresh token.

**JSON:**
```json
{
  "username": "$USERNAME",
  "password": "$PASSWORD"
}
```

**curl:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "$USERNAME", "password": "$PASSWORD"}'
```

---

### Refresh — `POST /api/token/refresh/`

Refresh your access token.

**JSON:**
```json
{
  "refresh": "$REFRESH_TOKEN"
}
```

**curl:**
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "$REFRESH_TOKEN"}'
```

---

### Supported Models — `GET /api/supported-models/?provider=$PROVIDER`

Returns a list of models supported by the specified provider (`openai`, `gemini`, or `inhouse`).

**curl:**
```bash
curl "http://localhost:8000/api/supported-models/?provider=gemini" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

### Chat Completion — `POST /api/chat/completions/?provider=$PROVIDER`

Submit a prompt and receive a response from the selected provider.

**JSON:**
```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "How is the weather on Venus?"}
  ],
  "stream": false
}
```

**curl:**
```bash
curl -X POST "http://localhost:8000/api/chat/completions/?provider=openai" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
        "model": "gpt-3.5-turbo",
        "messages": [
          {"role": "user", "content": "How is the weather on Venus?"}
        ],
        "stream": false
      }'
```

## Adding LLM providers
The API is highly configurable, and adding other providers (or removing them) is straightforward:
1. Create a relevant API key entry in .env and update env-template
2. Set the new API key value near the top of `project/settings.py` (follow the syntax of the other API key entries, e.g. `BLARG_KEY = config('BLARG_KEY')`)
3. Add the provider to the LLM_PROVIDERS dictionary at the bottom of `project/settings.py`
4. Create a provider module in `llm_api/providers/`. If the provider is OpenAI compatible, the module will be very similar to `llm_api/providers/openai.py`; otherwise you will have to consult the provider's documentation.

To remove a provider, just follow these instructions in reverse! Delete the provider, any references in settings.py, and the .env entry.

## The inhouse LLM
You can assume that the OpenAI and Gemini servers are up and running, but the inhouse LLM may not be. Check with the team before using it!

## License
[GNU General Public License v3](https://choosealicense.com/licenses/gpl-3.0/)
