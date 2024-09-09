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


}
}
