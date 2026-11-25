# Dify Customer Support Agent (Nimbus Coffee Co.)

Companion files for the Agentic AI Hub video **"Build an AI Customer Support Agent in Dify Without Writing Code."**

A no-code support bot built in [Dify](https://github.com/langgenius/dify). It answers from a FAQ knowledge base, looks up order status through an HTTP tool, and is published as an embeddable chat bubble. Everything runs on free software and free-tier models.

> Nimbus Coffee Co. is a fictional shop. The FAQ, orders, and email addresses are made up.

## What's inside

| Path | What it is |
|---|---|
| `faq/nimbus-coffee-faq.md` | The FAQ uploaded as the knowledge base |
| `dify-export/nimbus-support.ifpkg` | The Chatflow, exported with Dify's **Export App** (no secrets included) |
| `dify-export/app.yaml` | The same Chatflow as readable DSL (the file inside the `.ifpkg`) |
| `mock-api/` | A tiny order-status API (Python standard library) with 3 fictional orders, plus a Dockerfile and compose file |
| `widget-demo/index.html` | A demo shop page with Dify's chat-bubble snippet (`YOUR_TOKEN` placeholder) |
| `results/` | Real test results from the recorded build (hit tests, 7 chat tests, run log) |

## The Chatflow

```
User Input → Question Classifier
  ├─ FAQ        → Knowledge Retrieval → LLM (answer only from context) → Answer
  ├─ Order      → Parameter Extractor (order number) → HTTP GET /orders/<id> → If status = 200
  │                 ├─ yes → LLM (explain the order JSON) → Answer
  │                 └─ no  → fixed "I couldn't find that order" Answer
  └─ Other      → fixed polite Answer
Each answer LLM has retry + a fail branch to a free backup model.
```

Models (all on the Gemini API free tier, via the official Dify Gemini plugin):

- `gemini-4-hydrogen`: answers
- `gemini-3.5-flash-lite`: classifier, order-number extractor, and the free backup on the fail branch
- `gemini-embedding-001`: knowledge base embeddings

Don't select `gemini-4-carbon`, `gemini-4-argon`, or `gemini-4-neon`. Google's pricing page lists them as not available on the free tier.

**Free-tier limits are small.** During our build the Gemini API reported 5 requests/minute and 20 requests/day for `gemini-4-hydrogen` on our project. That's why the fail-branch backup exists. Check your own project's live limits in Google AI Studio.

## Run it yourself (self-hosted, free, no sign-up)

Official guide: <https://docs.dify.ai/en/self-host/deploy/quick-start/docker-compose>. You need Docker with Compose 2.35.0+, at least 2 CPU cores and 4 GiB RAM.

```bash
git clone --branch 1.20.0 --depth 1 https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
# put the output of `openssl rand -hex 32` into DIFY_AGENT_LOCAL_SANDBOX_AUTH_TOKEN in .env
docker compose up -d
docker compose ps        # wait for api to show (healthy)
```

Open `http://localhost/install`, create the admin account, then:

1. **Model provider.** Integrations → Model Provider → install **Gemini** → Add API Key (a free key from Google AI Studio). Set Default Models: System Reasoning `gemini-4-hydrogen`, Embedding `gemini-embedding-001`.
2. **Knowledge.** Knowledge → Create → Create a ready-to-use knowledge base → Import from file → `faq/nimbus-coffee-faq.md`. Index method High Quality, default chunking. Save and process.
3. **Mock API.** Self-hosted Dify sends HTTP-node traffic through its SSRF proxy, which blocks private addresses by default. Run the mock on the proxy's network and allow just that hostname:
   ```bash
   cd mock-api && docker compose up -d --build
   # in dify/docker/envs/infrastructure/ssrf-proxy.env add:
   #   SSRF_PROXY_ALLOW_PRIVATE_DOMAINS=nimbus-mock-api
   cd <dify>/docker && docker compose up -d ssrf_proxy
   ```
4. **Import the Chatflow.** Studio → Create → Import App → `dify-export/nimbus-support.ifpkg`. Exports don't carry linked knowledge bases, so open **Knowledge Retrieval** and select your Nimbus FAQ knowledge base. If you host the mock API elsewhere, edit the URL in **Order Status API**.
5. **Publish**, then Access Point → **Embed Into Site** → copy the chat-bubble snippet into `widget-demo/index.html` (replace `YOUR_TOKEN` in both places). Treat that token like a password and keep it out of git.

### Troubleshooting

- **API container keeps restarting with a Redis timeout.** Containers can't reach each other. Check that your host firewall's FORWARD chain allows Docker bridge traffic.
- **429 / "quota exceeded".** You hit a free-tier limit. Wait, or let the fail branch use the backup model. Don't add billing for a demo.
- **Dify Cloud instead of Docker?** It works too (free Sandbox, 200 one-time credits), but Cloud can't reach `localhost`, so host the mock orders on a public URL.

## Licence

MIT for the files in this repo. Dify is licensed separately by LangGenius; see its repository.
