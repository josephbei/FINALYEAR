@extends('layouts.app')

@section('content')
<h2>Login</h2>
<form method="POST" action="{{ url('login') }}">
  @csrf
  <div class="mb-3">
    <label class="form-label">Email</label>
    <input type="email" name="email" class="form-control" value="{{ old('email') }}">
  </div>
  <div class="mb-3">
    <label class="form-label">Password</label>
    <input type="password" name="password" class="form-control">
  </div>
  <button class="btn btn-primary">Login</button>
</form>
@endsection
