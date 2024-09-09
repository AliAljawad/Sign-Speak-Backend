<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;

class SpeechController extends Controller
{
    public function generateSpeech(Request $request)
    {
        $request->validate([
            'text' => 'required|string',
        ]);

}
