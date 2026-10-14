@extends('layouts.app')

@section('content')
<h2>Permission Requests</h2>
<p><a href="{{ route('permission-requests.create') }}" class="btn btn-success">New Request</a></p>
@if($requests->isEmpty())
  <p>No requests found.</p>
@else
  <table class="table">
    <thead>
      <tr><th>Destination</th><th>Departure</th><th>Return</th><th>Status</th><th></th></tr>
    </thead>
    <tbody>
      @foreach($requests as $r)
        <tr>
          <td>{{ $r->destination }}</td>
          <td>{{ $r->departure_time }}</td>
          <td>{{ $r->return_time }}</td>
          <td>{{ $r->status }}</td>
          <td><a href="{{ route('permission-requests.show', $r) }}" class="btn btn-sm btn-primary">View</a></td>
        </tr>
      @endforeach
    </tbody>
  </table>
@endif
@endsection
