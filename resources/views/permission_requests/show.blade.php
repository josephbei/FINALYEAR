@extends('layouts.app')

@section('content')
<h2>Permission Request</h2>
<div class="card">
  <div class="card-body">
    <h5 class="card-title">{{ $request->destination }}</h5>
    <p class="card-text">{{ $request->reason }}</p>
    <p><strong>Departure:</strong> {{ $request->departure_time }}</p>
    <p><strong>Return:</strong> {{ $request->return_time }}</p>
    <p><strong>Status:</strong> {{ $request->status }}</p>
  </div>
</div>
@endsection
