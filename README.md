# Mantle-of-Lies: Flask + Ollama LLM Mini Project

This mini project demonstrates how to connect a simple Flask web server to a locally running [Ollama LLM](https://ollama.com/) instance. The user interacts with the Flask web UI, sending a prompt to the Ollama LLM, and the response is printed back in the browser chat interface.

## Features

- **Web Chat UI**: Friendly web interface for chatting with a local Ollama LLM model.
- **Flask Backend**: Handles chat and forwards prompts to Ollama via HTTP.
- **Ollama Integration**: Works with any Ollama-supported model (default: `mistral`).
- **Docker Compose**: Both services are easily started and networked with a single command.

---

## Quick Start

### 1. Requirements

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)


### 2. Clone the Repository

```bash
git clone https://github.com/Prince-of-Nothing/Mantle-of-Lies.git
cd Mantle-of-Lies
```

### 3. Project Structure

```
.
├── flask_server/
│   └── app.py                # The main Flask application
│   └──Dockerfile
│   └──requirements.txt
├── docker-compose.yml        # Compose file for Flask & Ollama services
└── README.md
```

### 4. Start Both Services

```bash
docker compose up
```

This will:
- Start the Flask server at [http://localhost:5000](http://localhost:5000)
- Start an Ollama LLM service (It will create a container with a new ollama , because of reasons.)
## How it Works

- **User**: Types a prompt in the web form.
- **Flask**: Receives the prompt, sends it to the Ollama service via HTTP.
- **Ollama**: Processes the prompt with the selected model and returns a response.
- **Flask**: Displays the response in the UI chat box.

---

## Configuration

- By default, the Flask app sends requests to the Ollama service at `http://ollama-1:11434/api/generate` (Docker Compose network alias).
- To change the LLM model, edit the model name in the Flask Python file payload (default: `"mistral"`).
- To install a model{Mistral} you need to get the container id .

```bash
docker exec -it <container_name_or_id> bash
```
```bash
ollama pull mistral
```
```bash
exit
```
---



## License

MIT © Prince-of-Nothing

---

*This project was made as a template for integrating LLMs with Python web apps using Docker Compose. Feel free to adapt and extend!*
