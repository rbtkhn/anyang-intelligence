import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

test("server-renders the Grace Mar landing page", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>Grace Mar \| Coming Soon<\/title>/i);
  assert.match(html, /Grace Mar is home to thoughtfully built brands/);
  assert.match(html, /Grace Gems is the flagship jewelry brand of Grace Mar/);
  assert.match(html, /Jewelry for the stories we choose to keep\./);
  assert.match(html, /Contact details will be available here soon\./);
  assert.doesNotMatch(html, /<(form|input|textarea)\b/i);
  assert.doesNotMatch(html, /gtag|analytics|pixel|checkout|cart/i);
  assert.doesNotMatch(html, /codex-preview|Your site is taking shape|react-loading-skeleton/i);
});

test("keeps the first release inside the approved no-data boundary", async () => {
  const [page, layout, packageJson, readme] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/layout.tsx", import.meta.url), "utf8"),
    readFile(new URL("../package.json", import.meta.url), "utf8"),
    readFile(new URL("../README.md", import.meta.url), "utf8"),
  ]);

  assert.match(packageJson, /"name": "grace-mar-landing"/);
  assert.match(readme, /^# Grace Mar Landing Page/m);
  assert.match(layout, /title: "Grace Mar \| Coming Soon"/);
  assert.match(page, /Grace Mar/);
  assert.match(page, /Grace Gems/);

  for (const source of [page, layout, readme]) {
    assert.doesNotMatch(source, /codex-preview|Starter Project|vinext-starter|_sites-preview/i);
  }

  for (const source of [page, layout]) {
    assert.doesNotMatch(source, /<(form|input|textarea)\b/i);
    assert.doesNotMatch(source, /analytics|gtag|pixel|checkout|cart/i);
    assert.doesNotMatch(source, /Grace Mar LLC|limited liability|customer data/i);
  }
});
