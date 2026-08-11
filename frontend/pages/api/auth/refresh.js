import cookie from 'cookie'

export default async function handler(req, res){
  if (req.method !== 'POST') return res.status(405).end()
  const BACKEND = process.env.NEXT_PUBLIC_API_BACKEND || process.env.NEXT_PUBLIC_API_URL
  const cookies = cookie.parse(req.headers.cookie || '')
  const refresh = cookies.refresh_token
  if (!refresh) return res.status(401).json({ detail: 'No refresh token' })

  const r = await fetch(`${BACKEND}/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })
  const data = await r.json()
  if (!r.ok) return res.status(r.status).json(data)

  const accessMax = 24 * 60 * 60
  res.setHeader('Set-Cookie', cookie.serialize('access_token', data.access, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: accessMax,
  }))
  return res.status(200).json({ ok: true })
}
