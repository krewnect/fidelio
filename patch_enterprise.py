import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Unhide tab-mybusiness
old_tab = """<div class="nav-tab plan-business-only flex items-center px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-slate-900 hover:bg-slate-50 cursor-pointer transition-colors group" data-tab="tab-mybusiness" style="display:none;"><i class="fa-solid fa-building-columns w-6 text-slate-500 group-hover:text-fidelio-600 transition-colors"></i> Facturación & Negocio</div>"""
new_tab = """<div class="nav-tab plan-business-only flex items-center px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-slate-900 hover:bg-slate-50 cursor-pointer transition-colors group" data-tab="tab-mybusiness" id="nav-mybusiness"><i class="fa-solid fa-shield-halved w-6 text-slate-500 group-hover:text-fidelio-600 transition-colors"></i> Enterprise Settings</div>"""
content = content.replace(old_tab, new_tab)

# 2. Add Enterprise Settings UI section
enterprise_html = """
<!-- TAB ENTERPRISE SETTINGS -->
<section class="tab-content" id="tab-mybusiness">
    <div class="w-full max-w-7xl mx-auto px-4 md:px-8 pb-12 pt-8">
        <div class="mb-10">
            <div class="inline-flex items-center space-x-2 bg-slate-100 border border-slate-200 px-3 py-1 rounded-full mb-3">
                <i class="fa-solid fa-lock text-slate-500 text-[10px]"></i>
                <span class="text-[9px] font-bold text-slate-600 uppercase tracking-widest">Nivel Corporativo</span>
            </div>
            <h1 class="text-3xl font-black tracking-tight text-slate-900 mb-2">Seguridad y Datos (Enterprise)</h1>
            <p class="text-sm font-medium text-slate-500 max-w-3xl leading-relaxed">Configuraciones avanzadas de seguridad, autenticación corporativa y exportación de datos a Data Warehouses.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- SOC-2 Compliance Card -->
            <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-8 text-white relative overflow-hidden shadow-2xl col-span-1 lg:col-span-2 flex flex-col md:flex-row items-center justify-between">
                <div class="absolute right-0 top-0 w-64 h-full bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10 pointer-events-none"></div>
                <div class="relative z-10 max-w-lg mb-6 md:mb-0">
                    <div class="flex items-center space-x-3 mb-4">
                        <div class="bg-emerald-500/20 text-emerald-400 p-2 rounded-lg border border-emerald-500/30">
                            <i class="fa-solid fa-shield-check text-2xl"></i>
                        </div>
                        <h2 class="text-2xl font-black">Certificación SOC 2 Type II</h2>
                    </div>
                    <p class="text-slate-300 text-sm font-medium leading-relaxed mb-4">Fidelio cumple con los más altos estándares globales de seguridad de datos. Todos los PII y transacciones Fintech están encriptados end-to-end.</p>
                    <button class="bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold px-4 py-2 rounded-xl text-xs transition">
                        Descargar Reporte SOC-2 (PDF)
                    </button>
                </div>
                <div class="relative z-10 grid grid-cols-2 gap-4">
                    <div class="bg-black/20 p-4 rounded-2xl border border-white/5 text-center">
                        <i class="fa-brands fa-aws text-3xl text-slate-400 mb-2"></i>
                        <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">AWS KMS</p>
                    </div>
                    <div class="bg-black/20 p-4 rounded-2xl border border-white/5 text-center">
                        <i class="fa-solid fa-user-shield text-3xl text-emerald-400 mb-2"></i>
                        <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">GDPR / CCPA</p>
                    </div>
                </div>
            </div>

            <!-- Single Sign-On (SSO) -->
            <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <h3 class="text-lg font-black text-slate-900 mb-1">Single Sign-On (SSO)</h3>
                        <p class="text-xs text-slate-500 font-medium">Autenticación centralizada para tus empleados.</p>
                    </div>
                    <span class="bg-blue-50 text-blue-600 text-[10px] font-bold px-2 py-1 rounded-md border border-blue-100">SAML 2.0</span>
                </div>

                <div class="space-y-4">
                    <div class="flex items-center justify-between p-4 border border-slate-100 rounded-2xl hover:border-slate-300 transition cursor-pointer group">
                        <div class="flex items-center space-x-4">
                            <img src="https://cdn.worldvectorlogo.com/logos/okta-3.svg" class="h-6 grayscale group-hover:grayscale-0 transition">
                            <span class="text-sm font-bold text-slate-700">Okta Identity</span>
                        </div>
                        <i class="fa-solid fa-chevron-right text-slate-300 group-hover:text-slate-500"></i>
                    </div>
                    <div class="flex items-center justify-between p-4 border border-slate-100 rounded-2xl hover:border-slate-300 transition cursor-pointer group">
                        <div class="flex items-center space-x-4">
                            <img src="https://cdn.worldvectorlogo.com/logos/microsoft-azure-3.svg" class="h-6 grayscale group-hover:grayscale-0 transition">
                            <span class="text-sm font-bold text-slate-700">Azure Active Directory</span>
                        </div>
                        <i class="fa-solid fa-chevron-right text-slate-300 group-hover:text-slate-500"></i>
                    </div>
                </div>
            </div>

            <!-- BI & Data Warehouses -->
            <div class="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-fidelio-500"></div>
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <h3 class="text-lg font-black text-slate-900 mb-1">Conectores Big Data (BI)</h3>
                        <p class="text-xs text-slate-500 font-medium">Sincronización diaria a tu Data Warehouse.</p>
                    </div>
                    <div class="relative inline-block w-10 align-middle select-none transition duration-200 ease-in cursor-pointer">
                        <input type="checkbox" checked class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-2 appearance-none cursor-pointer border-transparent transition-transform duration-300 ease-in-out translate-x-5"/>
                        <label class="toggle-label block overflow-hidden h-5 rounded-full cursor-pointer transition-colors duration-300 ease-in-out bg-fidelio-500"></label>
                    </div>
                </div>

                <div class="space-y-4">
                    <div class="flex items-center justify-between p-4 border border-fidelio-200 bg-fidelio-50/50 rounded-2xl cursor-pointer group">
                        <div class="flex items-center space-x-4">
                            <img src="https://cdn.worldvectorlogo.com/logos/snowflake.svg" class="h-6">
                            <div>
                                <span class="text-sm font-bold text-slate-900 block">Snowflake DB</span>
                                <span class="text-[10px] text-fidelio-600 font-bold block">Conectado (Sync hace 2 hrs)</span>
                            </div>
                        </div>
                        <i class="fa-solid fa-circle-check text-fidelio-600"></i>
                    </div>
                    <div class="flex items-center justify-between p-4 border border-slate-100 rounded-2xl hover:border-slate-300 transition cursor-pointer group">
                        <div class="flex items-center space-x-4">
                            <img src="https://cdn.worldvectorlogo.com/logos/tableau-software.svg" class="h-6 grayscale group-hover:grayscale-0 transition">
                            <span class="text-sm font-bold text-slate-700">Tableau (Extract)</span>
                        </div>
                        <i class="fa-solid fa-chevron-right text-slate-300 group-hover:text-slate-500"></i>
                    </div>
                </div>
            </div>

        </div>
    </div>
</section>
"""

content = content.replace('<!-- MODAL: PREVIEW DE CAMPAÑA -->', enterprise_html + '\n<!-- MODAL: PREVIEW DE CAMPAÑA -->')

with open('index.html', 'w') as f:
    f.write(content)
print("Enterprise UI patched successfully")
