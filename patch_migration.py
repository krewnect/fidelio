import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Unhide and rename tab-global-db to tab-migration
old_tab = """<div class="nav-tab plan-business-only flex items-center px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-slate-900 hover:bg-slate-50 cursor-pointer transition-colors group" data-tab="tab-global-db" style="display:none;"><i class="fa-solid fa-earth-americas w-6 text-slate-500 group-hover:text-fidelio-600 transition-colors"></i> Global Data</div>"""
new_tab = """<div class="nav-tab plan-pro-only flex items-center px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-slate-900 hover:bg-slate-50 cursor-pointer transition-colors group" data-tab="tab-migration" id="nav-migration"><i class="fa-solid fa-wand-magic-sparkles w-6 text-slate-500 group-hover:text-fidelio-600 transition-colors"></i> Fidelio Switch <span class="ml-auto bg-slate-100 text-slate-500 py-0.5 px-2 rounded-full text-[8px] font-bold uppercase tracking-widest border border-slate-200">Migración</span></div>"""
content = content.replace(old_tab, new_tab)

# 2. Add Migration UI section
migration_html = """
<!-- TAB MIGRATION (FIDELIO SWITCH) -->
<section class="tab-content" id="tab-migration" x-data="{ step: 1, selectedPlatform: null, uploadProgress: 0, isUploading: false }">
    <div class="w-full max-w-5xl mx-auto px-4 md:px-8 pb-12 pt-8">
        <div class="text-center mb-12">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-3xl bg-fidelio-50 text-fidelio-600 mb-6 shadow-sm border border-fidelio-100">
                <i class="fa-solid fa-bolt text-2xl"></i>
            </div>
            <h1 class="text-4xl md:text-5xl font-black tracking-tight text-slate-900 mb-4">Fidelio Switch</h1>
            <p class="text-base text-slate-500 max-w-2xl mx-auto font-medium">¿Ya tienes un programa de lealtad? No pierdas a tus clientes ni su saldo. Importa tu base de datos actual en segundos y nosotros nos encargamos de enviarles su nueva Apple Wallet automáticamente.</p>
        </div>

        <!-- Step 1: Select Platform -->
        <div x-show="step === 1" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 transform translate-y-4" x-transition:enter-end="opacity-100 transform translate-y-0">
            <h3 class="text-sm font-black text-slate-400 uppercase tracking-widest mb-6 text-center">Selecciona tu proveedor actual</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <!-- Toast -->
                <button @click="selectedPlatform = 'toast'; step = 2" class="bg-white border-2 border-slate-100 hover:border-fidelio-400 hover:shadow-lg rounded-3xl p-6 transition-all group flex flex-col items-center">
                    <img src="https://cdn.worldvectorlogo.com/logos/toast-3.svg" class="h-10 opacity-60 group-hover:opacity-100 transition mb-4 grayscale group-hover:grayscale-0">
                    <span class="text-sm font-bold text-slate-700">Toast Loyalty</span>
                </button>
                <!-- Square -->
                <button @click="selectedPlatform = 'square'; step = 2" class="bg-white border-2 border-slate-100 hover:border-fidelio-400 hover:shadow-lg rounded-3xl p-6 transition-all group flex flex-col items-center">
                    <img src="https://cdn.worldvectorlogo.com/logos/square-inc.svg" class="h-10 opacity-60 group-hover:opacity-100 transition mb-4 grayscale group-hover:grayscale-0">
                    <span class="text-sm font-bold text-slate-700">Square</span>
                </button>
                <!-- Punchh -->
                <button @click="selectedPlatform = 'punchh'; step = 2" class="bg-white border-2 border-slate-100 hover:border-fidelio-400 hover:shadow-lg rounded-3xl p-6 transition-all group flex flex-col items-center">
                    <div class="w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center font-black text-xl mb-4 opacity-80 group-hover:opacity-100 group-hover:bg-rose-600 transition">P</div>
                    <span class="text-sm font-bold text-slate-700">Punchh</span>
                </button>
                <!-- CSV Custom -->
                <button @click="selectedPlatform = 'csv'; step = 2" class="bg-white border-2 border-slate-100 hover:border-fidelio-400 hover:shadow-lg rounded-3xl p-6 transition-all group flex flex-col items-center">
                    <div class="w-10 h-10 rounded-xl bg-slate-100 text-slate-400 group-hover:text-fidelio-600 flex items-center justify-center text-2xl mb-4 transition">
                        <i class="fa-solid fa-file-csv"></i>
                    </div>
                    <span class="text-sm font-bold text-slate-700">Otro (CSV / Excel)</span>
                </button>
            </div>
        </div>

        <!-- Step 2: Upload CSV -->
        <div x-show="step === 2" style="display:none;" class="bg-white border border-slate-200 rounded-3xl p-8 shadow-xl max-w-2xl mx-auto" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 transform translate-y-4" x-transition:enter-end="opacity-100 transform translate-y-0">
            <button @click="step = 1" class="text-xs font-bold text-slate-400 hover:text-slate-900 mb-6 flex items-center transition"><i class="fa-solid fa-arrow-left mr-2"></i> Cambiar Plataforma</button>
            
            <div class="border-2 border-dashed border-slate-200 hover:border-fidelio-400 rounded-2xl p-10 text-center transition group bg-slate-50 hover:bg-white cursor-pointer relative"
                 @click="if(!isUploading) { isUploading = true; let i = 0; let interval = setInterval(() => { i+=5; uploadProgress=i; if(i>=100) { clearInterval(interval); setTimeout(()=>step=3, 500) } }, 100); }">
                
                <div x-show="!isUploading">
                    <div class="w-16 h-16 bg-white shadow-sm rounded-full flex items-center justify-center mx-auto mb-4 text-slate-400 group-hover:text-fidelio-600 transition">
                        <i class="fa-solid fa-cloud-arrow-up text-2xl"></i>
                    </div>
                    <h3 class="text-lg font-black text-slate-900 mb-1">Sube tu archivo exportado</h3>
                    <p class="text-xs text-slate-500 font-medium">Arrastra el archivo CSV de <span class="capitalize" x-text="selectedPlatform"></span> aquí o haz clic para explorar.</p>
                </div>

                <div x-show="isUploading" class="w-full">
                    <div class="flex justify-between text-xs font-bold text-slate-700 mb-2">
                        <span>Procesando e importando...</span>
                        <span x-text="uploadProgress + '%'"></span>
                    </div>
                    <div class="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
                        <div class="bg-fidelio-600 h-2.5 rounded-full transition-all duration-200" :style="'width: ' + uploadProgress + '%'"></div>
                    </div>
                </div>
            </div>
            
            <div class="mt-6 p-4 bg-amber-50 rounded-xl flex items-start space-x-3 border border-amber-100">
                <i class="fa-solid fa-lightbulb text-amber-500 mt-0.5"></i>
                <div>
                    <p class="text-xs font-bold text-amber-800">Fidelio Mapea Automáticamente</p>
                    <p class="text-[10px] text-amber-700/80 mt-1 font-medium leading-relaxed">Nuestro algoritmo detectará las columnas: Nombre, Teléfono, Correo, Puntos Actuales y LTV. No te preocupes por el formato, nosotros lo ajustamos.</p>
                </div>
            </div>
        </div>

        <!-- Step 3: Success & Actions -->
        <div x-show="step === 3" style="display:none;" class="bg-white border border-slate-200 rounded-3xl p-10 shadow-2xl max-w-2xl mx-auto text-center relative overflow-hidden" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 transform scale-95" x-transition:enter-end="opacity-100 transform scale-100">
            <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5 pointer-events-none"></div>
            
            <div class="w-20 h-20 bg-emerald-50 text-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm border border-emerald-100">
                <i class="fa-solid fa-check text-4xl"></i>
            </div>
            <h2 class="text-2xl font-black text-slate-900 mb-2">¡Migración Exitosa!</h2>
            <p class="text-sm font-medium text-slate-500 mb-8">Se han importado <span class="font-bold text-slate-900">4,281 clientes</span> y sus saldos de lealtad intactos.</p>
            
            <div class="bg-slate-50 border border-slate-100 rounded-2xl p-6 text-left mb-8">
                <h3 class="text-xs font-black text-slate-900 uppercase tracking-widest mb-4">Siguiente Acción Recomendada:</h3>
                <div class="flex items-start space-x-4">
                    <div class="w-10 h-10 bg-fidelio-100 text-fidelio-600 rounded-xl flex items-center justify-center shrink-0">
                        <i class="fa-solid fa-paper-plane"></i>
                    </div>
                    <div>
                        <p class="text-sm font-bold text-slate-900">Campaña SMS "Welcome to Fidelio"</p>
                        <p class="text-xs text-slate-500 mt-1 font-medium mb-3">Envíale a toda tu base migrada un mensaje de texto con su nueva Apple Wallet y un regalo de bienvenida para asegurar que la descarguen.</p>
                        <button class="bg-fidelio-600 hover:bg-fidelio-700 text-white font-bold px-4 py-2 rounded-xl text-xs transition shadow-md">
                            Lanzar Campaña SMS
                        </button>
                    </div>
                </div>
            </div>
            
            <button @click="step = 1; uploadProgress = 0; isUploading = false;" class="text-xs font-bold text-slate-400 hover:text-slate-900 transition">Volver al inicio</button>
        </div>

    </div>
</section>
"""

content = content.replace('<!-- TAB MIGRATION (FIDELIO SWITCH) -->', migration_html)
if '<!-- TAB MIGRATION (FIDELIO SWITCH) -->' not in content:
    # Append to the end of main
    content = content.replace('<!-- MODAL: PREVIEW DE CAMPAÑA -->', migration_html + '\n<!-- MODAL: PREVIEW DE CAMPAÑA -->')

with open('index.html', 'w') as f:
    f.write(content)
print("Migration UI patched successfully")
