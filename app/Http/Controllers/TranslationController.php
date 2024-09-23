<?php

namespace App\Http\Controllers;

use App\Models\Translation;
use Auth;
use Illuminate\Http\Request;
use Log;

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
        // Ensure the user is authenticated
        $this->middleware('auth:api');
    
        // Log the request for debugging
        Log::info('store request received', ['request' => $request->all()]);
    
        // Validate incoming request
        $validatedData = $request->validate([
            'input_type' => 'required|in:video,image,live',
            'translated_text' => 'required|string',
            'translated_audio' => 'nullable|file|mimes:mp3,wav',
            'input_data' => 'nullable|file|mimes:mp4,jpg,jpeg,png|max:100000',
        ]);
    
        // Get the authenticated user
        $user = Auth::user();
    
        // Save the input file and get the path
        $inputDataPath = null;
        if ($request->hasFile('input_data')) {
            $inputDataPath = $request->file('input_data')->store('uploads/input_data', 'public');
        }
    
        // Save the translated audio file and get the path
        $translatedAudioPath = null;
        if ($request->hasFile('translated_audio')) {
            $translatedAudioPath = $request->file('translated_audio')->store('uploads/translated_audio', 'public');
        }
    
        // Create a new translation entry in the database
        try {
            $translation = Translation::create([
                'user_id' => $user->id,
                'input_type' => $validatedData['input_type'],
                'input_data' => $inputDataPath,
            ]);
    
            // Save the translated text in the `translated_text` table
            $translation->translatedText()->create([
                'text' => $validatedData['translated_text'],
            ]);
    
            // Save the translated audio path in the `translated_audio` table (if present)
            if ($translatedAudioPath) {
                $translation->translatedAudio()->create([
                    'audio_path' => $translatedAudioPath,
                ]);
            }
    
            Log::info('Translation saved', ['translation' => $translation]);
        } catch (\Exception $e) {
            Log::error('Error saving translation', ['error' => $e->getMessage()]);
            return response()->json(['error' => 'Failed to save translation'], 500);
        }
    
        // Return a success response
        return response()->json([
            'success' => true,
            'message' => 'Translation saved successfully',
            'translation' => $translation
        ], 201);
    }
    
    /**
     * Display the specified resource.
     */
    public function show()
{
    $user = Auth::user();
    \Log::error('User ID:', ['id' => $user->id]);

    // Load translations along with related translated text and audio
    $translations = Translation::with(['translatedText', 'translatedAudio'])
                    ->where('user_id', $user->id)
                    ->get();

    if ($translations->isEmpty()) {
        return response()->json(['message' => 'No translations found'], 404);
    }

    // Transform the translations to include only the required fields
    $response = $translations->map(function ($translation) {
        return [
            'id' => $translation->id,
            'input_type' => $translation->input_type,
            'input_data' => $translation->input_data,
            'translated_text' => $translation->translatedText->text,
            'translated_audio' => $translation->translatedAudio ? $translation->translatedAudio->audio_path : null, // Actual audio path
            'created_at' => $translation->created_at,
            'updated_at' => $translation->updated_at,
        ];
    });

    \Log::error('Translations:', ['translations' => $response]);

    return response()->json($response);
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
        $validatedData = $request->validate([
            'input_type' => 'sometimes|in:video,image,live',
            'input_data' => 'sometimes|nullable|file|mimes:mp4,jpg,jpeg,png|max:100000',
            'translated_text' => 'sometimes|string',
            'translated_audio' => 'sometimes|file|mimes:mp3,wav',
        ]);
    
        // Update the translation
        if ($request->hasFile('input_data')) {
            $inputDataPath = $request->file('input_data')->store('uploads/input_data', 'public');
            $translation->input_data = $inputDataPath;
        }
    
        $translation->update($validatedData);
    
        // Update the translated text
        if ($request->filled('translated_text')) {
            $translation->translatedText->update([
                'text' => $validatedData['translated_text'],
            ]);
        }
    
        // Update the translated audio (if present)
        if ($request->hasFile('translated_audio')) {
            $translatedAudioPath = $request->file('translated_audio')->store('uploads/translated_audio', 'public');
            $translation->translatedAudio->update([
                'audio_path' => $translatedAudioPath,
            ]);
        }
    
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
