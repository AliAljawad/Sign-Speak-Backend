<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Translation extends Model
{
    use HasFactory;
    protected $fillable=[
        'user_id',
        'translated_text',
        'voice_id',
        'input_type',
        'input_data',
    ];
    public function user()
    {
        return $this->belongsTo(User::class);
    }
    public function voice()
    {
        return $this->belongsTo(Voice::class);
    }

}
