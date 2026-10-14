@extends('layouts.app')

@section('content')
<h2>Dashboard</h2>
@if($requests->isEmpty())
  <p>No recent permission requests.</p>
@else
  <ul class="list-group">
    @foreach($requests as $r)
      <li class="list-group-item">
        <strong>{{ $r->destination }}</strong> — {{ $r->status }}
        <span class="float-end">{{ $r->departure_time ? $r->departure_time->format('Y-m-d H:i') : '' }}</span>
      </li>
    @endforeach
  </ul>
@endif
@endsection
