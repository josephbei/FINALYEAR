<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Student extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'parent_id',
        'name',
        'form_class',
        'year_of_study',
        'hostel_room_no',
        'admission_year',
        'admission_number',
    ];

    protected $casts = [
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];

    // Relations
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function parent()
    {
        return $this->belongsTo(ParentModel::class, 'parent_id');
    }

    public function permissionRequests()
    {
        return $this->hasMany(PermissionRequest::class, 'student_id');
    }

    // Scopes
    public function scopeByFormClass($query, $formClass)
    {
        return $query->where('form_class', $formClass);
    }

    public function scopeByYear($query, $year)
    {
        return $query->where('year_of_study', $year);
    }

    public function scopeByAdmissionYear($query, $admissionYear)
    {
        return $query->where('admission_year', $admissionYear);
    }
}
