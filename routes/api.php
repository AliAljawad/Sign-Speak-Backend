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
Route::resource('translations',TranslationController::class);