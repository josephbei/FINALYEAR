<?php

use Illuminate\Support\Facades\Route;

// Admin routes for managing teachers
Route::middleware(['auth', 'is_admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::resource('teachers', App\Http\Controllers\Admin\TeacherController::class);
});
