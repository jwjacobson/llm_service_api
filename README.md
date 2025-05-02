# LLM Service API
The LLM Service API is built using Django and Django REST Framework and provides access to OpenAI, Google Gemini, and our in-house LLM. It is easily configurable and extensible to allow the addition of other LLM providers.

## Requirements
- [Python 3.13](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
Note: these instructions assume you are using uv for project and dependency management. If you use another tool, the commands you run will be slightly different (no 'uv') and you'll have to do extra work to create a virtual environment, install dependencies, etc..
- [OpenAI API key](https://platform.openai.com/api-keys) (to interact with OpenAI LLMs)
- [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) (to interact with Gemini LLMs)

## Installation
1. [Clone this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2. Navigate to the llm_service_api directory
3. Copy the contents of env-template into a file named `.env` in the project's root directory, and fill in appropriate values without quotation marks. This app uses `python-decouple` to manage environment variables, and will not run unless they are set.
4. Run `uv sync` to synchronize the project dependecies with your environment
5. Run `uv run python manage.py migrate` to apply the initial database migrations

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

**curl:**:
```bash
curl http://127.0.0.1:8000/
```
**Sample response:**
```json
{
"message":"Welcome to the LLM API!"
}
```
---

### Signup — `POST /api/signup/`

Creates a user.

**JSON:**
```json
{
  "username": "charming_user",
  "password": "secure_pwd"
}
```

**curl:**
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "charming_user", "password": "secure_pwd"}'
```

**Sample response:**
```json
{
"message":"User created successfully"
}
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

**Sample response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
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

**Sample response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
}
```

---

### Supported Models — `GET /api/supported-models/?provider=$PROVIDER`

Returns a list of models supported by the specified provider (`openai`, `gemini`, or `inhouse`).

**curl:**
```bash
curl "http://localhost:8000/api/supported-models/?provider=gemini" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Sample response:**
```json
{
     "models": ["gemini-pro", "gemini-pro-vision" ...]
}
```

---

### Chat Completion — `POST /api/chat/completions/?provider=$PROVIDER`

Submit a prompt and receive a response from the selected provider (`openai`, `gemini`, or `inhouse`).

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
**Sample response**:
```json
{"id":"chatcmpl-BSpaQfs3CEkCL79NzcNP8gVrIAGsg","choices":[{"finish_reason":"stop","index":0,"logprobs":null,"message":{"content":"The weather on Venus is extremely inhospitable, with temperatures reaching up to 900 degrees Fahrenheit (475 degrees Celsius). Venus also has a thick atmosphere made up mostly of carbon dioxide and clouds of sulfuric acid, creating a runaway greenhouse effect that traps heat and makes it the hottest planet in our solar system. The atmospheric pressure on Venus is about 92 times that of Earth's surface pressure, which is equivalent to being nearly a kilometer underwater on Earth. Additionally, Venus experiences hurricane-force winds that can reach speeds of up to 224 miles per hour (360 kilometers per hour) in its upper atmosphere.","refusal":null,"role":"assistant","annotations":[],"audio":null,"function_call":null,"tool_calls":null}}],"created":1746211182,"model":"gpt-3.5-turbo-0125","object":"chat.completion","service_tier":"default","system_fingerprint":null,"usage":{"completion_tokens":123,"prompt_tokens":14,"total_tokens":137,"completion_tokens_details":{"accepted_prediction_tokens":0,"audio_tokens":0,"reasoning_tokens":0,"rejected_prediction_tokens":0},"prompt_tokens_details":{"audio_tokens":0,"cached_tokens":0}}}
```

**Tip:** if you just want to play with the LLM endpoints without dealing with authentication, you can comment out the following lines in the relevant function of views.py:
 ```python
 authentication_classes = [JWTAuthentication]
 permission_classes = [IsAuthenticated]
 ```

But be careful!

## Adding LLM providers
The API is highly configurable, and adding other providers (or removing them) is straightforward:
1. Create a relevant API key entry in .env and update env-template
2. Set the new API key value near the top of `project/settings.py` (follow the syntax of the other API key entries, e.g. `BLARG_KEY = config('BLARG_KEY')`)
3. Add the provider to the LLM_PROVIDERS dictionary at the bottom of `project/settings.py` (again, follow the existing syntax)
4. Create a provider module in `llm_api/providers/`. If the provider is OpenAI compatible, the module will be very similar to `llm_api/providers/openai.py`; otherwise you will have to consult the provider's documentation.

Now you will have a new provider, the name of which will be the same as the corresponding key in the LLM_PROVIDERS dict of settings.py.

To remove a provider, just follow these instructions in reverse! Delete the provider, any references in settings.py, and the .env entry.

## The inhouse LLM
You can assume that the OpenAI and Gemini servers are up and running, but the inhouse LLM may not be. Check with the team before trying to use it!

## License
[GNU General Public License v3](https://choosealicense.com/licenses/gpl-3.0/)

## Feedback
- For bug reports, please open an issue with a description of what you expected vs what you got
- For suggestions, please open an issue with a description of the desired behavior
- For gratuitous praise, please send a toot to https://fosstodon.org/@jeffjacobson
- Thanks for reading this far!
