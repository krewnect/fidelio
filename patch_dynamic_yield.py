import re

with open('index.html', 'r') as f:
    content = f.read()

dynamic_yield_html = """
            <!-- Campaña 4: Dynamic Yield (Cashback Dinámico) -->
            <div class="bg-gradient-to-br from-fidelio-900 to-slate-900 border-2 border-fidelio-500 rounded-3xl p-6 relative overflow-hidden transition-all shadow-[0_10px_30px_rgba(139,92,246,0.2)]">
                <div class="absolute -right-4 -top-4 w-32 h-32 bg-fidelio-500/20 rounded-full blur-2xl pointer-events-none"></div>
                <div class="flex justify-between items-start mb-4 relative z-10">
                    <div class="w-12 h-12 rounded-2xl bg-fidelio-500/20 text-fidelio-300 flex items-center justify-center text-xl border border-fidelio-500/30">
                        <i class="fa-solid fa-money-bill-trend-up"></i>
                    </div>
                    <div class="relative inline-block w-12 align-middle select-none transition duration-200 ease-in cursor-pointer">
                        <input type="checkbox" checked class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-2 appearance-none cursor-pointer border-transparent transition-transform duration-300 ease-in-out translate-x-6"/>
                        <label class="toggle-label block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-300 ease-in-out bg-fidelio-500"></label>
                    </div>
                </div>
                <h3 class="text-lg font-black text-white mb-1 relative z-10">Surge Cashback (Dynamic Yield)</h3>
                <p class="text-xs text-fidelio-200 mb-4 font-medium relative z-10">Sube el cashback automáticamente para llenar el restaurante en horas muertas. Cierra la llave al llenarse.</p>
                <div class="space-y-3 relative z-10">
                    <div class="bg-black/30 p-3 rounded-xl border border-white/10">
                        <label class="text-[10px] font-bold text-fidelio-300 uppercase tracking-widest block mb-1">Multiplicador de Hora Muerta</label>
                        <select class="w-full bg-transparent font-medium text-sm text-white focus:outline-none">
                            <option>Subir Cashback a 20% (Max)</option>
                            <option>Subir Cashback a 15%</option>
                            <option>Subir Cashback a 10%</option>
                        </select>
                    </div>
                    <div class="bg-black/30 p-3 rounded-xl border border-white/10">
                        <label class="text-[10px] font-bold text-fidelio-300 uppercase tracking-widest block mb-1">Push de Geocerca (3km)</label>
                        <textarea class="w-full bg-transparent font-medium text-sm text-white focus:outline-none resize-none" rows="2">⚡ Surge: 20% de Cashback en todas tus compras si vienes en los próximos 90 minutos.</textarea>
                    </div>
                </div>
            </div>
"""

# Find the end of the Autopilot grid and insert the new card
if '<!-- Campaña 4: Dynamic Yield' not in content:
    content = content.replace('<!-- Campaña 3: Horas Muertas -->', dynamic_yield_html + '\n            <!-- Campaña 3: Horas Muertas -->')

with open('index.html', 'w') as f:
    f.write(content)
print("Dynamic Yield UI patched successfully")
