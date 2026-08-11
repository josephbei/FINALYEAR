import cookie from 'cookie'

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end()
  const { username, password } = req.body
  const BACKEND = process.env.NEXT_PUBLIC_API_BACKEND || process.env.NEXT_PUBLIC_API_URL
  const r = await fetch(`${BACKEND}/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  const data = await r.json()
  if (!r.ok) return res.status(r.status).json(data)

  const accessMax = 24 * 60 * 60
  const refreshMax = 7 * 24 * 60 * 60
  res.setHeader('Set-Cookie', [
    cookie.serialize('access_token', data.access, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: accessMax,
    }),
    cookie.serialize('refresh_token', data.refresh, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: refreshMax,
    }),
  ])
  return res.status(200).json({ ok: true })
}
