import {useState} from 'react'

export default function ParentRegister(){
  const [form, setForm] = useState({username:'', password:'', name:'', email:'', phone:''})
  const [message, setMessage] = useState('')
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

  async function submit(e){
    e.preventDefault()
    const res = await fetch(`${api}/parents/register/`, {
      method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(form)
    })
    if(res.ok){
      setMessage('Registered successfully. You can now login on the main site.')
    } else {
      const data = await res.json()
      setMessage('Error: ' + JSON.stringify(data))
    }
  }

  return (
    <div style={{padding:20}}>
      <h1>Parent Register</h1>
      <form onSubmit={submit}>
        <input placeholder="username" value={form.username} onChange={e=>setForm({...form, username:e.target.value})} /><br/>
        <input placeholder="password" type="password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} /><br/>
        <input placeholder="name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} /><br/>
        <input placeholder="email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} /><br/>
        <input placeholder="phone" value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} /><br/>
        <button type="submit">Register</button>
      </form>
      <p>{message}</p>
    </div>
  )
}
