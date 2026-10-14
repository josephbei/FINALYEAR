<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up()
    {
        Schema::create('permission_requests', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('student_id')->nullable();
            $table->unsignedBigInteger('parent_id')->nullable();
            $table->text('reason');
            $table->string('destination');
            $table->timestamp('departure_time')->nullable();
            $table->timestamp('return_time')->nullable();
            $table->string('hostel_room_no')->nullable();
            $table->string('status')->default('pending');
            $table->string('request_type')->default('normal');
            $table->string('approved_by_role')->nullable();
            $table->unsignedBigInteger('approved_by_id')->nullable();
            $table->text('rejection_reason')->nullable();
            $table->string('escalated_to')->nullable();
            $table->unsignedBigInteger('escalated_by_id')->nullable();
            $table->unsignedBigInteger('teacher_approved_by')->nullable();
            $table->timestamp('parent_notified_at')->nullable();
            $table->timestamps();

            $table->index('parent_id');
            $table->index('student_id');
        });
    }

    public function down()
    {
        Schema::dropIfExists('permission_requests');
    }
};
