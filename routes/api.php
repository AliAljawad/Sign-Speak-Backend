<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\TranslationController;
use App\Http\Controllers\UserController;
use Illuminate\Support\Facades\Route;

Route::controller(AuthController::class)->group(function () {
    Route::post('login', 'login');
    Route::post('register', 'register');
    Route::post('logout', 'logout');
    Route::post('refresh', 'refresh');
});

Route::resource('users', UserController::class);

Route::put('/updateUser', [UserController::class, 'update']);
Route::post('/upload-image', [UserController::class, 'uploadImage']);

Route::get('getUser',[UserController::class,'show']);
Route::resource('translations',TranslationController::class);
Route::get('/verify-token', function (Request $request) {
    $user = Auth::user();
    
    if ($user) {
        return response()->json(['valid' => true]);
    } else {
        return response()->json(['valid' => false], 401);
    }
});