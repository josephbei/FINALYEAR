import {useState, useEffect} from 'react'
import { apiFetch } from '../lib/api'

export default function CreatePermission(){
  const [students, setStudents] = useState([])
  const [form, setForm] = useState({student_id:'', permission_type:'emergency', reason:''})
  const [msg, setMsg] = useState('')

  useEffect(()=>{
    apiFetch('students/')
      .then(setStudents)
      .catch(e=>{ console.error(e); window.location.href = '/login' })
  },[])

  async function submit(e){
    e.preventDefault()
    try{
      await apiFetch('permissions/', { method: 'POST', body: { student_id: form.student_id, permission_type: form.permission_type, reason: form.reason } })
      setMsg('Request created')
    }catch(err){
      setMsg('Error creating request')
    }
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
