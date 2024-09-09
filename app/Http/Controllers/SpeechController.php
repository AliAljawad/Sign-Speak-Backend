<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Log;

class SpeechController extends Controller
{
    public function generateSpeech(Request $request)
    {
        $request->validate([
            'text' => 'required|string',
        ]);
$text = $request->input('text');
$voiceId = config('services.elevenLabs.voice_id');
$apiURL = "https://api.elevenlabs.io/v1/text-to-speech/{$voiceId}";
$apiKey = config('services.elevenLabs.api_key');
Log::error('this is the voiceid:', [$voiceId, 'this is the api key:', $apiKey]);

$response = Http::withHeaders([
    'xi-api-key' => $apiKey,
    'Content-Type' => 'application/json',
    'Accept' => 'audio/mpeg',
])->post($apiURL, [
    'text' => $text,
    'model_id' => 'eleven_monolingual_v1',
    'voice_settings' => [
        'stability' => 0,
        'similarity_boost' => 0,
        'style' => 0,
        'use_speaker_boost' => true,
    ],
]);

}
}
