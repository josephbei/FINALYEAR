<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\PermissionRequest;

class PermissionRequestController extends Controller
{
    public function index()
    {
        $requests = PermissionRequest::where('parent_id', auth()->id())->orWhere('student_id', auth()->id())->latest()->get();
        return view('permission_requests.index', compact('requests'));
    }

    public function create()
    {
        return view('permission_requests.create');
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'reason' => 'required|string',
            'destination' => 'required|string',
            'departure_time' => 'required|date',
            'return_time' => 'required|date',
            'request_type' => 'required|string',
        ]);

        $data['parent_id'] = auth()->id();
        $data['status'] = PermissionRequest::STATUS_PENDING;

        PermissionRequest::create($data);

        return redirect()->route('permission-requests.index')->with('success', 'Request submitted.');
    }

    public function show(PermissionRequest $permission_request)
    {
        return view('permission_requests.show', ['request' => $permission_request]);
    }

    public function edit(PermissionRequest $permission_request)
    {
        return view('permission_requests.edit', ['request' => $permission_request]);
    }

    public function update(Request $request, PermissionRequest $permission_request)
    {
        $data = $request->validate([
            'reason' => 'required|string',
            'destination' => 'required|string',
            'departure_time' => 'required|date',
            'return_time' => 'required|date',
            'request_type' => 'required|string',
        ]);

        $permission_request->update($data);

        return redirect()->route('permission-requests.index')->with('success', 'Request updated.');
    }

    public function destroy(PermissionRequest $permission_request)
    {
        $permission_request->delete();
        return redirect()->route('permission-requests.index')->with('success', 'Request deleted.');
    }
}
