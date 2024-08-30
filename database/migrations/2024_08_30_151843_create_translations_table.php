<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('translations', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->nullable()->constrained()->onDelete('cascade')->onUpdate('cascade');
            $table->foreignId('voice_id')->nullable()->constrained()->onDelete('set null')->onUpdate('cascade');
            $table->enum('input_type', ['video', 'image', 'live']);
            $table->string('input_data')->nullable();
            $table->text('translated_text');
            $table->string('translated_audio')->nullable();
            $table->timestamp('translation_date')->useCurrent();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('translations');
    }
};
