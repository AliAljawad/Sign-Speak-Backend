<?php

namespace App\Http\Controllers;
use Auth;
use Hash;
use App\Models\User;
use Illuminate\Http\Request;
use Log;

class UserController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $users = User::all();
        return response()->json($users);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8',
        ]);

        $user = User::create([
            'name' => $validatedData['name'],
            'email' => $validatedData['email'],
            'password' => Hash::make($validatedData['password']),
        ]);

        return response()->json($user, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Request $request)
{
    // Get the currently authenticated user
    $user = Auth::user();

    if (!$user) {
        return response()->json(['message' => 'User not found'], 404);
    }

    return response()->json($user);
}

    /**
     * Update the specified resource in storage.
     * */
    public function update(Request $request)
{
    $user = Auth::user();

    try {
        $request->validate([
            'name' => 'sometimes|string|max:255',
            'email' => 'sometimes|string|email|max:255|unique:users,email,' . $user->id,
            'password' => 'nullable|string|min:8',
             'profile_image' => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048',
        ]);

        // Update the name, email, and password if provided
        if ($request->has('name')) {
            $user->name = $request->input('name');
        }

        if ($request->has('email')) {
            $user->email = $request->input('email');
        }

        if ($request->filled('password')) {
            $user->password = bcrypt($request->input('password'));
        }

        // Handle the image upload
        if ($request->hasFile('profile_image')) {
            \Log::info('Image file received');
            $image = $request->file('profile_image');
            $imagePath = $image->store('profile_images', 'public');
            $user->profile_image = $imagePath;
        } else {
            \Log::error('No image received');
        }
        $user->save();

        return response()->json(['message' => 'Profile updated successfully'], 200);
    } catch (\Exception $e) {
        Log::error('Error updating profile: ' . $e->getMessage());
        return response()->json(['message' => 'An error occurred while updating the profile.'], 500);
    }
}
    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        $user = User::find($id);

        if (!$user) {
            return response()->json(['message' => 'User not found'], 404);
        }

        $user->delete();

        return response()->json(['message' => 'User deleted successfully']);

    }
}
