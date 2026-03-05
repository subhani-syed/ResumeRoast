const API_BASE = process.env.INTERNAL_API_URL;

async function handler(req, { params }) {
  const path = params.path.join("/");
  const url = `${API_BASE}/${path}`;

  const headers = new Headers(req.headers);
  headers.delete("host");

  const res = await fetch(url, {
    method: req.method,
    headers,
    body: req.body,
  });

  return new Response(res.body, {
    status: res.status,
    headers: res.headers,
  });
}

export {
  handler as GET,
  handler as POST,
  handler as PUT,
  handler as DELETE,
  handler as PATCH,
};
