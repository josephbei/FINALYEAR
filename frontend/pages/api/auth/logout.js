import cookie from 'cookie'

export default async function handler(req, res){
  if (req.method !== 'POST') return res.status(405).end()
  // Clear cookies
  res.setHeader('Set-Cookie', [
    cookie.serialize('access_token', '', { httpOnly: true, secure: process.env.NODE_ENV === 'production', sameSite: 'lax', path: '/', maxAge: 0 }),
    cookie.serialize('refresh_token', '', { httpOnly: true, secure: process.env.NODE_ENV === 'production', sameSite: 'lax', path: '/', maxAge: 0 }),
  ])
  return res.status(200).json({ ok: true })
}
