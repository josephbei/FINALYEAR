import {useEffect, useState} from 'react'
import { apiFetch } from '../lib/api'

export default function ParentDashboard(){
  const [students, setStudents] = useState([])
  const [err, setErr] = useState('')

  useEffect(()=>{
    apiFetch('students/')
      .then(data=>setStudents(data))
      .catch(e=>{
        console.error(e); setErr('Please login')
        if (typeof window !== 'undefined') window.location.href = '/login'
      })
  },[])

  return (
    <div style={{padding:20}}>
      <h1>Parent Dashboard</h1>
      {err && <p>{err}</p>}
      <h3>Your children</h3>
      <ul>
        {students.map(s => <li key={s.id}>{s.name} ({s.reg_number})</li>)}
      </ul>
      <p><a href="/create-permission">Request permission</a></p>
    </div>
  )
}
