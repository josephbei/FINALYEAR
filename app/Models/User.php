<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable
{
    use HasFactory, Notifiable, HasApiTokens;

    protected $fillable = [
        'name',
        'email',
        'password',
        'role',
        'category',
        'is_warned',
        'service_denied',
        'changed_password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'is_warned' => 'boolean',
        'service_denied' => 'boolean',
        'changed_password' => 'boolean',
    ];

    // Relations
    public function parent()
    {
        return $this->hasOne(ParentModel::class);
    }

    public function teacher()
    {
        return $this->hasOne(Teacher::class);
    }

    public function student()
    {
        return $this->hasOne(Student::class);
    }

    public function approvedPermissions()
    {
        return $this->hasMany(PermissionRequest::class, 'approved_by_id');
    }

    // Accessors
    public function getRoleDisplayAttribute()
    {
        return ucfirst($this->role);
    }

    // Scopes
    public function scopeByRole($query, $role)
    {
        return $query->where('role', $role);
    }

    public function scopeWarned($query)
    {
        return $query->where('is_warned', true);
    }

    public function scopeServiceDenied($query)
    {
        return $query->where('service_denied', true);
    }
}
