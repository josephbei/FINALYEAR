export async function apiFetch(path, options={}){
  const rp = `/api/proxy/${path}`
  const res = await fetch(rp, {
    method: options.method || 'GET',
    headers: { 'Content-Type': 'application/json' },
    body: options.body ? JSON.stringify(options.body) : undefined,
    credentials: 'include',
  })
  if (res.status === 401){
    // try refresh
    const r = await fetch('/api/auth/refresh', { method: 'POST', credentials: 'include' })
    if (r.ok){
      // retry original request
      const retry = await fetch(rp, {
        method: options.method || 'GET',
        headers: { 'Content-Type': 'application/json' },
        body: options.body ? JSON.stringify(options.body) : undefined,
        credentials: 'include',
      })
      const jd = await retry.json().catch(()=>null)
      if (!retry.ok) throw jd || { detail: 'Error' }
      return jd
    }
    throw { detail: 'Unauthorized' }
  }
  const data = await res.json().catch(()=>null)
  if (!res.ok) throw data || { detail: 'Error' }
  return data
}
