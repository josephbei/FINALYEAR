import cookie from 'cookie'

export default async function handler(req, res) {
  const { path } = req.query
  const BACKEND = process.env.NEXT_PUBLIC_API_BACKEND || process.env.NEXT_PUBLIC_API_URL
  const url = `${BACKEND}/${(path || []).join('/')}`

  // read access token from cookie
  const cookies = cookie.parse(req.headers.cookie || '')
  const access = cookies.access_token

  const headers = { 'Content-Type': req.headers['content-type'] || 'application/json' }
  if (access) headers['authorization'] = `Bearer ${access}`

  const backendRes = await fetch(url, {
    method: req.method,
    headers,
    body: ['GET','HEAD'].includes(req.method) ? undefined : JSON.stringify(req.body || {}),
  })

  const text = await backendRes.text()
  res.status(backendRes.status)
  backendRes.headers.forEach((value, key) => {
    if (key.toLowerCase() === 'set-cookie') return
    res.setHeader(key, value)
  })
  res.send(text)
}
