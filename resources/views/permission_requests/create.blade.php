@extends('layouts.app')

@section('content')
<h2>New Permission Request</h2>
<form method="POST" action="{{ route('permission-requests.store') }}">
  @csrf
  <div class="mb-3">
    <label class="form-label">Destination</label>
    <input name="destination" class="form-control" value="{{ old('destination') }}">
  </div>
  <div class="mb-3">
    <label class="form-label">Reason</label>
    <textarea name="reason" class="form-control">{{ old('reason') }}</textarea>
  </div>
  <div class="mb-3">
    <label class="form-label">Departure Time</label>
    <input type="datetime-local" name="departure_time" class="form-control" value="{{ old('departure_time') }}">
  </div>
  <div class="mb-3">
    <label class="form-label">Return Time</label>
    <input type="datetime-local" name="return_time" class="form-control" value="{{ old('return_time') }}">
  </div>
  <div class="mb-3">
    <label class="form-label">Request Type</label>
    <select name="request_type" class="form-control">
      <option value="normal">Normal</option>
      <option value="emergency">Emergency</option>
    </select>
  </div>
  <button class="btn btn-primary">Submit</button>
</form>
@endsection
