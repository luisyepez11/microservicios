import { createClient } from '@supabase/supabase-js';

const Clientesupabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,       
  import.meta.env.VITE_SUPABASE_ANON_KEY
);
console.log(import.meta.env.VITE_SUPABASE_URL)

export default Clientesupabase;