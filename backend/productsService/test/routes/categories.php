<?php

use Illuminate\Support\Facades\Route;
use App\Services\CategoriesService;

Route::get('/Categories', function () {
    $categoriesService = new CategoriesService();
    return $categoriesService->getCategories();
});

Route::post('/newCategory', function () {
    $categoriesService = new CategoriesService();
    $name = request('name');

    return $categoriesService->createCategory($name);
});

Route::put('/updateCategory/{id}', function ($id) {
    $categoriesService = new CategoriesService();
    $name = request('name');

    return $categoriesService->editCategory($id, $name);
})->whereNumber('id');

Route::delete('/deleteCategory/{id}', function ($id) {
    $categoriesService = new CategoriesService();
    return $categoriesService->deleteCategory($id);
})->whereNumber('id');

?>
