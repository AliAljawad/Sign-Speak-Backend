<?php

namespace App\Http\Controllers;

use App\Models\Translation;
use Illuminate\Http\Request;

class TranslationController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $translations = Translation::all();
        return response()->json($translations);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $request->validate([
            'user_id' => 'required|exists:users,id',
            'voice_id' => 'nullable|exists:voices,id',
            'input_type' => 'required|in:video,image,live',
            'input_data' => 'nullable|string',
            'translated_text' => 'required|string',
            'translated_audio' => 'nullable|string',
        ]);

        // Create a new translation record
        $translation = Translation::create([
            'user_id' => $request->user_id,
            'voice_id' => $request->voice_id,
            'input_type' => $request->input_type,
            'input_data' => $request->input_data,
            'translated_text' => $request->translated_text,
            'translated_audio' => $request->translated_audio,
        ]);

        return response()->json($translation, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show($id)
    {
        $translation = Translation::find($id);
    
        if (!$translation) {
            return response()->json(['message' => 'Translation not found'], 404);
        }
    
        return response()->json($translation);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        $translation = Translation::find($id);

        if (!$translation) {
            return response()->json(['message' => 'Translation not found'], 404);
        }

        // Validate the incoming request data
        $request->validate([
            'user_id' => 'sometimes|exists:users,id',
            'voice_id' => 'sometimes|nullable|exists:voices,id',
            'input_type' => 'sometimes|in:video,image,live',
            'input_data' => 'sometimes|nullable|string',
            'translated_text' => 'sometimes|string',
            'translated_audio' => 'sometimes|nullable|string',
        ]);

        // Update the translation with the validated data
        $translation->update($request->all());

        return response()->json($translation);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        //
    }
}
