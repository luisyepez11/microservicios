import app from './src/app.js';
import { PORT } from './src/config.js';

app.listen(PORT,()=>{
    console.log(`funcionando ando en puerto http://localhost:${PORT}`)
})