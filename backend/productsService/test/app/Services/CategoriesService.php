<?php

namespace App\Services;

use Illuminate\Support\Facades\DB;

class CategoriesService{
    public function createCategory($name){
        if (DB::table('Categories')->where('name', $name)->exists()) {
            return "Category already exists";
        }

        $category_id = random_int(1, 9999);
        while (true){
            if (!DB::table('Categories')->where('category_id', $category_id)->exists()) {
                break;
            }
            $category_id = random_int(1, 9999);
        }

        $categoryData = [
            'category_id' => $category_id,
            'name' => $name,
        ];

        $this->loadCategoryToDB($categoryData);
        return $category_id;
    }

    private function loadCategoryToDB(array $category){
        return DB::table('Categories')->insertGetId($category);
    }

    public function getCategories(){
        return DB::table('Categories');
    }

    public function editCategory($id, $name){
        return DB::table('Categories')->where('category_id', $id)->update([
            'name' => $name,
        ]);
    }

    public function deleteCategory($id){
        return DB::table('Categories')->where('category_id', $id)->delete();
    }
}
?>
