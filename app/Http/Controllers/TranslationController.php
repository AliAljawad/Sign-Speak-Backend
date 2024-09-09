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
        // Log the request for debugging
        Log::info('store request received', ['request' => $request->all()]);
        // Validate incoming request
    $validatedData = $request->validate([
    'input_type' => 'required|in:video,image,live',
    'translated_text' => 'required|string',
    'translated_audio' => 'nullable|file|mimes:mp3,wav',
    'input_data' => 'nullable|file|mimes:mp4,jpg,jpeg,png|max:100000',
]);

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
         // Find the translation by ID
         $translation = Translation::find($id);

         if (!$translation) {
             return response()->json(['message' => 'Translation not found'], 404);
         }
 
         // Delete the translation
         $translation->delete();
 
         return response()->json(['message' => 'Translation deleted successfully']);
     
    }
}
