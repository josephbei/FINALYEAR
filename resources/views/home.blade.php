@extends('layouts.app')

@section('content')
<div class="jumbotron">
    <h1 class="display-5">Welcome to {{ config('app.name') }}</h1>
    <p class="lead">School Permission Management System - Parent &amp; Admin portal.</p>
    @guest
      <p><a class="btn btn-primary" href="{{ route('register') }}" role="button">Get started</a></p>
    @else
      <p><a class="btn btn-primary" href="{{ route('dashboard') }}" role="button">Go to dashboard</a></p>
    @endguest
</div>
@endsection
