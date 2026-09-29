/**
 * ==============================================================================
 * CLOUDFLARE WORKER PER A LA QUINIELA DE L'AE LLUÏSOS DE GRÀCIA
 * ==============================================================================
 * Aquest codi s'ha de desplegar al panell de Cloudflare Workers.
 *
 * PASSOS PER A LA CONFIGURACIÓ:
 * 1. Crea un nou Worker a Cloudflare (ex: 'kiniela-worker').
 * 2. Copia i enganxa aquest codi al teu Worker.
 * 3. Crea una base de dades KV a Cloudflare anomenada 'EL_TEU_KV' (o el nom que vulguis).
 * 4. A les opcions del Worker (Settings > Variables > KV Namespace Bindings):
 *    - Enllaça la variable 'EL_TEU_KV' al teu KV Namespace creat.
 * 5. Canvia 'Access-Control-Allow-Origin' per la URL del teu GitHub Pages o deixa '*' per permetre-ho.
 * 6. Copia l'URL del Worker (ex: https://kiniela-worker.el-teu-subdomini.workers.dev)
 *    i enganxa-la a 'CLOUDFLARE_WORKER_URL' a 'static/js/data.js'.
 */

export default {
  async fetch(request, env) {
    // Configurar capçaleres per permetre peticions des del teu web de GitHub
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*", // Pots canviar-ho per la URL del teu GitHub Pages
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    // Respondre correctament a les comprovacions prèvies del navegador (Preflight)
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    // 1. ESCRIURE DADES (POST)
    if (request.method === "POST") {
      try {
        const body = await request.json();
        // Guardem el text a la KV amb la clau "les_meves_dades"
        // 'EL_TEU_KV' s'ha d'enllaçar al panell de Cloudflare
        await env.EL_TEU_KV.put("les_meves_dades", JSON.stringify(body));
        
        return new Response(JSON.stringify({ status: "Guardat!" }), {
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      } catch (err) {
        return new Response("Error de format", { status: 400, headers: corsHeaders });
      }
    }

    // 2. LLEGIR DADES (GET)
    if (request.method === "GET") {
      const dades = await env.EL_TEU_KV.get("les_meves_dades");
      return new Response(dades || "{}", {
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }

    return new Response("Mètode no permès", { status: 405, headers: corsHeaders });
  }
};
