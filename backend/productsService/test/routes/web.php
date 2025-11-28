<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

require __DIR__.'/products.php';
require __DIR__.'/categories.php';
require __DIR__.'/cart.php';
