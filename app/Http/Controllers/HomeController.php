<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\PermissionRequest;

class HomeController extends Controller
{
    public function index()
    {
        return view('home');
    }

    public function dashboard()
    {
        $requests = auth()->check() ? PermissionRequest::latest()->take(10)->get() : collect();
        return view('dashboard', compact('requests'));
    }
}
