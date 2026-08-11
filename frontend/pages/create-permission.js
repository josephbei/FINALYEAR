import {useState, useEffect} from 'react'

export default function CreatePermission(){
  const [students, setStudents] = useState([])
  const [form, setForm] = useState({student_id:'', permission_type:'emergency', reason:''})
  const [msg, setMsg] = useState('')
  const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

  useEffect(()=>{
    fetch(`${api}/students/`).then(r=>r.json()).then(setStudents)
  },[])

  async function submit(e){
    e.preventDefault()
    const payload = {student_id: form.student_id, permission_type: form.permission_type, reason: form.reason}
    const res = await fetch(`${api}/permissions/`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)})
    if(res.ok){setMsg('Request created') } else {setMsg('Error')}
  }

  return (
    <div style={{padding:20}}>
      <h1>Create Permission</h1>
      <form onSubmit={submit}>
        <select value={form.student_id} onChange={e=>setForm({...form, student_id:e.target.value})}>
          <option value="">Select student</option>
          {students.map(s=> <option key={s.id} value={s.id}>{s.name} ({s.reg_number})</option>)}
        </select><br/>
        <label>Type</label>
        <select value={form.permission_type} onChange={e=>setForm({...form, permission_type:e.target.value})}>
          <option value="normal">Normal</option>
          <option value="emergency">Emergency</option>
        </select><br/>
        <textarea placeholder="reason" value={form.reason} onChange={e=>setForm({...form, reason:e.target.value})}></textarea><br/>
        <button type="submit">Submit</button>
      </form>
      <p>{msg}</p>
    </div>
  )
}
