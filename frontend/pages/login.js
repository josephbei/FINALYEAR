import {useState} from 'react'

export default function Login(){
  const [form, setForm] = useState({username:'', password:''})
  const [msg, setMsg] = useState('')

  async function submit(e){
    e.preventDefault()
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(form)
    })
    if(res.ok){
      // redirect to parent dashboard
      window.location.href = '/parent-dashboard'
    } else {
      const d = await res.json().catch(()=>({detail:'error'}))
      setMsg(d.detail || 'Login failed')
    }
  }

  return (
    <div style={{padding:20}}>
      <h1>Login</h1>
      <form onSubmit={submit}>
        <input placeholder="username" value={form.username} onChange={e=>setForm({...form, username:e.target.value})} /><br/>
        <input placeholder="password" type="password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} /><br/>
        <button type="submit">Login</button>
      </form>
      <p>{msg}</p>
    </div>
  )
}
