import re

with open('index.html', 'r') as f:
    content = f.read()

autopilot_html = """
<!-- TAB AUTOPILOT (FIDELITO AI) -->
<section class="tab-content" id="tab-autopilot" x-data="{ autopilotActive: true, weatherEnabled: true, inactiveEnabled: true, timeEnabled: false }">
    <div class="w-full max-w-7xl mx-auto px-4 md:px-8 pb-12">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 mb-8 relative z-10 w-full">
            <div>
                <p class="text-[11px] font-black text-fidelio-600 uppercase tracking-widest mb-2"><i class="fa-solid fa-robot mr-2 opacity-50"></i>FIDELITO IA</p>
                <h1 class="text-4xl font-black tracking-tight text-slate-900 mb-2">Piloto Automático</h1>
                <p class="text-sm font-medium text-slate-500 max-w-2xl leading-relaxed">Deja que la inteligencia artificial rescate clientes perdidos y lance campañas dinámicas basándose en el clima o en horas muertas. Cero esfuerzo, máxima monetización.</p>
            </div>
            <div class="flex-shrink-0">
                <button class="bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm px-6 py-3 rounded-xl transition shadow-lg flex items-center">
                    <i class="fa-solid fa-floppy-disk mr-2"></i> Guardar Motor
                </button>
            </div>
        </div>

        <!-- Master Switch -->
        <div class="bg-gradient-to-r from-fidelio-600 to-fidelio-800 rounded-3xl p-8 text-white flex flex-col md:flex-row items-center justify-between mb-8 shadow-[0_10px_40px_rgba(139,92,246,0.3)] relative overflow-hidden">
            <i class="fa-solid fa-microchip text-9xl opacity-10 absolute -right-10 -bottom-10"></i>
            <div>
                <h2 class="text-2xl font-black mb-1">Motor de IA Predictiva</h2>
                <p class="text-fidelio-100 text-sm font-medium">El sistema monitorea tu base de datos 24/7 y dispara Web Push Notifications directamente al Apple Wallet de tus clientes cuando se cumplen las condiciones.</p>
            </div>
            <div class="mt-6 md:mt-0 relative z-10 flex flex-col items-center">
                <div class="relative inline-block w-16 align-middle select-none transition duration-200 ease-in mb-2 cursor-pointer" @click="autopilotActive = !autopilotActive">
                    <input type="checkbox" x-model="autopilotActive" class="toggle-checkbox absolute block w-8 h-8 rounded-full bg-white border-4 appearance-none cursor-pointer border-transparent transition-transform duration-300 ease-in-out" :class="autopilotActive ? 'translate-x-8 shadow-[0_0_15px_rgba(255,255,255,0.8)]' : 'translate-x-0 bg-slate-300'"/>
                    <label class="toggle-label block overflow-hidden h-8 rounded-full cursor-pointer transition-colors duration-300 ease-in-out" :class="autopilotActive ? 'bg-emerald-400' : 'bg-slate-400/50'"></label>
                </div>
                <span class="text-xs font-black uppercase tracking-widest" x-text="autopilotActive ? 'SISTEMA ACTIVO' : 'SISTEMA APAGADO'" :class="autopilotActive ? 'text-emerald-300' : 'text-slate-300'"></span>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" :class="!autopilotActive ? 'opacity-50 pointer-events-none transition' : 'transition'">
            
            <!-- Campaña 1: Churn (Rescate) -->
            <div class="bg-white border-2 rounded-3xl p-6 relative overflow-hidden transition-all" :class="inactiveEnabled ? 'border-fidelio-400 shadow-xl' : 'border-slate-200'">
                <div class="flex justify-between items-start mb-4">
                    <div class="w-12 h-12 rounded-2xl bg-rose-50 text-rose-500 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-heart-crack"></i>
                    </div>
                    <div class="relative inline-block w-12 align-middle select-none transition duration-200 ease-in cursor-pointer" @click="inactiveEnabled = !inactiveEnabled">
                        <input type="checkbox" x-model="inactiveEnabled" class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-2 appearance-none cursor-pointer border-transparent transition-transform duration-300 ease-in-out" :class="inactiveEnabled ? 'translate-x-6' : 'translate-x-0'"/>
                        <label class="toggle-label block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-300 ease-in-out" :class="inactiveEnabled ? 'bg-fidelio-500' : 'bg-slate-200'"></label>
                    </div>
                </div>
                <h3 class="text-lg font-black text-slate-900 mb-1">Rescate de Fugas (Churn)</h3>
                <p class="text-xs text-slate-500 mb-4 font-medium">Detecta clientes que cruzaron el umbral de abandono y los trae de vuelta.</p>
                <div class="space-y-3">
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Condición IA</label>
                        <select class="w-full bg-transparent font-medium text-sm text-slate-900 focus:outline-none">
                            <option>Si no visitan en 21 días</option>
                            <option>Si no visitan en 30 días</option>
                            <option>Si no visitan en 60 días</option>
                        </select>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Mensaje Push Nativo</label>
                        <textarea class="w-full bg-transparent font-medium text-sm text-slate-900 focus:outline-none resize-none" rows="2">¡Te extrañamos! Usa este código de rescate para un café gratis hoy.</textarea>
                    </div>
                </div>
            </div>

            <!-- Campaña 2: Clima -->
            <div class="bg-white border-2 rounded-3xl p-6 relative overflow-hidden transition-all" :class="weatherEnabled ? 'border-fidelio-400 shadow-xl' : 'border-slate-200'">
                <div class="flex justify-between items-start mb-4">
                    <div class="w-12 h-12 rounded-2xl bg-blue-50 text-blue-500 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-cloud-showers-heavy"></i>
                    </div>
                    <div class="relative inline-block w-12 align-middle select-none transition duration-200 ease-in cursor-pointer" @click="weatherEnabled = !weatherEnabled">
                        <input type="checkbox" x-model="weatherEnabled" class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-2 appearance-none cursor-pointer border-transparent transition-transform duration-300 ease-in-out" :class="weatherEnabled ? 'translate-x-6' : 'translate-x-0'"/>
                        <label class="toggle-label block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-300 ease-in-out" :class="weatherEnabled ? 'bg-fidelio-500' : 'bg-slate-200'"></label>
                    </div>
                </div>
                <h3 class="text-lg font-black text-slate-900 mb-1">Disparador Climático</h3>
                <p class="text-xs text-slate-500 mb-4 font-medium">Conectado a la API del clima local. Lanza promociones si las ventas bajan por el clima.</p>
                <div class="space-y-3">
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Condición IA</label>
                        <select class="w-full bg-transparent font-medium text-sm text-slate-900 focus:outline-none">
                            <option>Si hay Tormenta / Lluvia Fuerte</option>
                            <option>Si hace más de 35°C</option>
                            <option>Si hace menos de 10°C</option>
                        </select>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Mensaje Push Nativo</label>
                        <textarea class="w-full bg-transparent font-medium text-sm text-slate-900 focus:outline-none resize-none" rows="2">¡Olvídate de la lluvia! Pide por delivery con envío gratis usando tu Wallet.</textarea>
                    </div>
                </div>
            </div>

            <!-- Campaña 3: Horas Muertas -->
            <div class="bg-white border-2 rounded-3xl p-6 relative overflow-hidden transition-all" :class="timeEnabled ? 'border-fidelio-400 shadow-xl' : 'border-slate-200'">
                <div class="flex justify-between items-start mb-4">
                    <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-500 flex items-center justify-center text-xl">
                        <i class="fa-solid fa-hourglass-empty"></i>
                    </div>
                    <div class="relative inline-block w-12 align-middle select-none transition duration-200 ease-in cursor-pointer" @click="timeEnabled = !timeEnabled">
                        <input type="checkbox" x-model="timeEnabled" class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-2 appearance-none cursor-pointer border-transparent transition-transform duration-300 ease-in-out" :class="timeEnabled ? 'translate-x-6' : 'translate-x-0'"/>
                        <label class="toggle-label block overflow-hidden h-6 rounded-full cursor-pointer transition-colors duration-300 ease-in-out" :class="timeEnabled ? 'bg-fidelio-500' : 'bg-slate-200'"></label>
                    </div>
                </div>
                <h3 class="text-lg font-black text-slate-900 mb-1">Inyector de Horas Muertas</h3>
                <p class="text-xs text-slate-500 mb-4 font-medium">El algoritmo detecta bajones en el tráfico y dispara cupones relámpago.</p>
                <div class="space-y-3">
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Condición IA</label>
                        <select class="w-full bg-transparent font-medium text-sm text-slate-900 focus:outline-none">
                            <option>Martes de 4 PM a 6 PM</option>
                            <option>Lunes todo el día</option>
                            <option>Automático (Cuando IA detecte caída)</option>
                        </select>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-1">Mensaje Push Nativo</label>
                        <textarea class="w-full bg-transparent font-medium text-sm text-slate-900 focus:outline-none resize-none" rows="2">¡Flash Promo! Doble puntuación si vienes en los próximos 60 minutos.</textarea>
                    </div>
                </div>
            </div>

        </div>
    </div>
</section>
"""

content = content.replace('<!-- TOAST NOTIFICATIONS -->', autopilot_html + '\n<!-- TOAST NOTIFICATIONS -->')

with open('index.html', 'w') as f:
    f.write(content)
print("Autopilot UI patched successfully")
