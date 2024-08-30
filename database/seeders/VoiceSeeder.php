<?php

namespace Database\Seeders;

use App\Models\Voice;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class VoiceSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        Voice::factory()->count(20)->create();
    }
}
