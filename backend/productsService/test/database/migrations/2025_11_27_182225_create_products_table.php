<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        // If thw table does not exist, create it
        if (!Schema::hasTable('Products')) {
            Schema::create('Products', function (Blueprint $table) {
                $table->id('id');
                $table->foreignId('category_id');
                $table->string('name', 50);
                $table->string('description', 255);
                $table->string('image_url', 255);
                $table->integer('price');
            });
        }
    }


    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
