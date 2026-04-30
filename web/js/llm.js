/**
 * LLM provider abstraction.
 *
 * Each provider exposes a single method:
 *   async *chat(messages, systemPrompt)  →  yields text chunks as they stream in
 *
 * messages: [{ role: 'user'|'assistant', content: string }, ...]
 *
 * Config is persisted to localStorage under CONFIG_KEY.
 */

const CONFIG_KEY = 'clb-llm-config';

// ── Config helpers ─────────────────────────────────────────────────────────

export function loadLLMConfig() {
  try { return JSON.parse(localStorage.getItem(CONFIG_KEY) ?? '{}'); }
  catch { return {}; }
}

export function saveLLMConfig(cfg) {
  localStorage.setItem(CONFIG_KEY, JSON.stringify(cfg));
}

export function createProvider(cfg) {
  if (cfg.provider === 'gemini') return new GeminiProvider(cfg.gemini ?? {});
  if (cfg.provider === 'groq')   return new GroqProvider(cfg.groq ?? {});
  if (cfg.provider === 'ollama') return new OllamaProvider(cfg.ollama ?? {});
  return null;
}

// ── Gemini ─────────────────────────────────────────────────────────────────

class GeminiProvider {
  constructor({ apiKey = '', model = 'gemini-2.0-flash' } = {}) {
    this.apiKey = apiKey;
    this.model  = model;
  }

  async *chat(messages, systemPrompt) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/`
              + `${this.model}:streamGenerateContent?key=${this.apiKey}&alt=sse`;

    const contents = messages.map(m => ({
      role:  m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }],
    }));

    const body = { contents };
    if (systemPrompt) body.systemInstruction = { parts: [{ text: systemPrompt }] };

    const res = await fetch(url, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`Gemini ${res.status}: ${await res.text()}`);

    yield* _parseSSE(res.body, data =>
      data.candidates?.[0]?.content?.parts?.[0]?.text ?? '');
  }
}

// ── Groq ───────────────────────────────────────────────────────────────────

class GroqProvider {
  constructor({ apiKey = '', model = 'llama-3.1-8b-instant' } = {}) {
    this.apiKey = apiKey;
    this.model  = model;
  }

  async *chat(messages, systemPrompt) {
    const all = systemPrompt
      ? [{ role: 'system', content: systemPrompt }, ...messages]
      : messages;

    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method:  'POST',
      headers: { 'Authorization': `Bearer ${this.apiKey}`, 'Content-Type': 'application/json' },
      body:    JSON.stringify({ model: this.model, messages: all, stream: true }),
    });
    if (!res.ok) throw new Error(`Groq ${res.status}: ${await res.text()}`);

    yield* _parseSSE(res.body, data =>
      data.choices?.[0]?.delta?.content ?? '');
  }
}

// ── Ollama ─────────────────────────────────────────────────────────────────
// Requires Ollama started with OLLAMA_ORIGINS="*" (or the page origin) to
// allow browser requests from a different host/port.

class OllamaProvider {
  constructor({ baseUrl = 'http://localhost:11434', model = 'llama3.2' } = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.model   = model;
  }

  async *chat(messages, systemPrompt) {
    const all = systemPrompt
      ? [{ role: 'system', content: systemPrompt }, ...messages]
      : messages;

    const res = await fetch(`${this.baseUrl}/api/chat`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ model: this.model, messages: all, stream: true }),
    });
    if (!res.ok) throw new Error(`Ollama ${res.status}: ${await res.text()}`);

    // Ollama streams newline-delimited JSON (not SSE)
    const reader  = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();
      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const data = JSON.parse(line);
          const text = data.message?.content ?? '';
          if (text) yield text;
          if (data.done) return;
        } catch { /* skip malformed lines */ }
      }
    }
  }
}

// ── SSE parser (shared by Gemini + Groq) ──────────────────────────────────

async function* _parseSSE(body, extract) {
  const reader  = body.getReader();
  const decoder = new TextDecoder();
  let buf = '';
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const lines = buf.split('\n');
    buf = lines.pop();
    for (const line of lines) {
      if (!line.startsWith('data:')) continue;
      const payload = line.slice(5).trim();
      if (payload === '[DONE]') return;
      try {
        const text = extract(JSON.parse(payload));
        if (text) yield text;
      } catch { /* skip malformed */ }
    }
  }
}
