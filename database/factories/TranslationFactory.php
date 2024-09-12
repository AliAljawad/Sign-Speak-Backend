<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Translation>
 */
class TranslationFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'input_type' => $this->faker->randomElement(['video', 'image']),
            'input_data' => $this->faker->filePath(), 
            'translated_text' => $this->faker->sentence(),
            'translated_audio' => $this->faker->filePath(), 
        ];
    }
}
