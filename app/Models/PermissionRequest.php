<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class PermissionRequest extends Model
{
    use HasFactory;

    protected $table = 'permission_requests';

    protected $fillable = [
        'student_id',
        'parent_id',
        'reason',
        'destination',
        'departure_time',
        'return_time',
        'hostel_room_no',
        'status',
        'request_type',
        'approved_by_role',
        'approved_by_id',
        'rejection_reason',
        'escalated_to',
        'escalated_by_id',
        'teacher_approved_by',
        'parent_notified_at',
    ];

    protected $casts = [
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
        'departure_time' => 'datetime',
        'return_time' => 'datetime',
        'parent_notified_at' => 'datetime',
    ];

    // Relations
    public function student()
    {
        return $this->belongsTo(Student::class, 'student_id');
    }

    public function parent()
    {
        return $this->belongsTo(ParentModel::class, 'parent_id');
    }

    public function approvedBy()
    {
        return $this->belongsTo(User::class, 'approved_by_id');
    }

    public function teacherApproved()
    {
        return $this->belongsTo(Teacher::class, 'teacher_approved_by');
    }

    public function escalatedBy()
    {
        return $this->belongsTo(User::class, 'escalated_by_id');
    }

    // Scopes
    public function scopeApproved($query)
    {
        return $query->where('status', 'approved');
    }

    public function scopeRejected($query)
    {
        return $query->where('status', 'rejected');
    }

    public function scopePending($query)
    {
        return $query->where('status', 'pending');
    }

    public function scopeActive($query)
    {
        return $query->where('status', 'active');
    }

    public function scopeEscalated($query)
    {
        return $query->whereNotNull('escalated_to');
    }

    public function scopeNormalRequest($query)
    {
        return $query->where('request_type', 'normal');
    }

    public function scopeEmergency($query)
    {
        return $query->where('request_type', 'emergency');
    }

    // Constants
    const STATUS_PENDING = 'pending';
    const STATUS_APPROVED = 'approved';
    const STATUS_REJECTED = 'rejected';
    const STATUS_ACTIVE = 'active';

    const TYPE_NORMAL = 'normal';
    const TYPE_EMERGENCY = 'emergency';

    const ESCALATED_TO_DISCIPLINE = 'discipline';
    const ESCALATED_TO_HEADMASTER = 'headmaster';
}
