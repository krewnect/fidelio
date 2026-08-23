import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Unhide tab-bank
old_bank_tab = """<div class="nav-tab plan-business-only flex items-center px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-slate-900 hover:bg-slate-50 cursor-pointer transition-colors group" data-tab="tab-bank" style="display:none;"><i class="fa-solid fa-piggy-bank w-6 text-slate-500 group-hover:text-fidelio-600 transition-colors"></i> The Bank</div>"""
new_bank_tab = """<div class="nav-tab plan-business-only flex items-center px-3 py-2.5 rounded-lg text-sm font-medium text-slate-500 hover:text-slate-900 hover:bg-slate-50 cursor-pointer transition-colors group" data-tab="tab-bank" id="nav-bank"><i class="fa-solid fa-building-columns w-6 text-slate-500 group-hover:text-fidelio-600 transition-colors"></i> The Bank</div>"""
content = content.replace(old_bank_tab, new_bank_tab)

# 2. Add Bank UI Section
bank_html = """
<!-- TAB THE BANK (FINTECH) -->
<section class="tab-content" id="tab-bank" x-data="{ issueGiftCard: false, giftAmount: 500, customerPhone: '' }">
    <div class="w-full max-w-7xl mx-auto px-4 md:px-8 pb-12">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 mb-8 relative z-10 w-full">
            <div>
                <p class="text-[11px] font-black text-fidelio-600 uppercase tracking-widest mb-2"><i class="fa-solid fa-vault mr-2 opacity-50"></i>FIDELIO FINTECH</p>
                <h1 class="text-4xl font-black tracking-tight text-slate-900 mb-2">The Bank</h1>
                <p class="text-sm font-medium text-slate-500 max-w-2xl leading-relaxed">Emite tarjetas de regalo digitales (Stored Value), obtén liquidez inmediata por adelantado y solicita capital de crecimiento respaldado por tus ventas futuras.</p>
            </div>
            <div class="flex-shrink-0">
                <button @click="issueGiftCard = true" class="bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm px-6 py-3 rounded-xl transition shadow-lg flex items-center">
                    <i class="fa-solid fa-plus mr-2"></i> Emitir Gift Card
                </button>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- Liquidez Inmediata (Flotante) -->
            <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-6 text-white relative overflow-hidden shadow-2xl">
                <div class="absolute -right-4 -top-4 text-white/5 text-8xl">
                    <i class="fa-solid fa-money-bill-wave"></i>
                </div>
                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1 relative z-10">Flotante Total (Unspent Value)</p>
                <h3 class="text-4xl font-black text-white relative z-10 mb-1">$42,500<span class="text-lg text-slate-400">.00</span></h3>
                <p class="text-xs text-emerald-400 font-medium relative z-10"><i class="fa-solid fa-arrow-trend-up mr-1"></i> +$5,200 este mes</p>
                <div class="mt-6 pt-4 border-t border-white/10 relative z-10">
                    <p class="text-xs text-slate-300 leading-tight">Dinero real que tus clientes ya te pagaron por adelantado en Tarjetas de Regalo, pero aún no han consumido en sucursal.</p>
                </div>
            </div>

            <!-- Capital Pre-aprobado -->
            <div class="bg-white border-2 border-fidelio-400 rounded-3xl p-6 relative overflow-hidden shadow-[0_10px_30px_rgba(139,92,246,0.15)] col-span-1 md:col-span-2 flex flex-col md:flex-row items-center gap-6">
                <div class="flex-1">
                    <div class="inline-flex items-center space-x-2 bg-fidelio-50 border border-fidelio-100 px-3 py-1 rounded-full mb-3">
                        <i class="fa-solid fa-bolt text-fidelio-600 text-[10px]"></i>
                        <span class="text-[9px] font-bold text-fidelio-600 uppercase tracking-widest">Fidelio Capital</span>
                    </div>
                    <h3 class="text-2xl font-black text-slate-900 mb-2">Oferta de Capital Activa</h3>
                    <p class="text-sm text-slate-600 font-medium mb-4">Basado en tu LTV y retención, Fidelio puede adelantarte flujo de efectivo hoy. El repago se cobra automáticamente como un porcentaje de tus futuras recargas de Gift Cards.</p>
                    <button class="bg-fidelio-600 hover:bg-fidelio-700 text-white font-bold px-6 py-2.5 rounded-xl text-sm transition shadow-md">
                        Aceptar $150,000 MXN
                    </button>
                </div>
                <div class="w-full md:w-48 shrink-0 bg-slate-50 rounded-2xl p-4 border border-slate-100 text-center">
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Tasa Fija</p>
                    <p class="text-2xl font-black text-slate-800 mb-2">9.5%</p>
                    <p class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Repago Automático</p>
                    <p class="text-lg font-black text-slate-800">12%<span class="text-xs text-slate-500 font-medium"> de ventas diarias</span></p>
                </div>
            </div>
        </div>

        <!-- Ledger de Transacciones Fintech -->
        <div class="bg-white border border-slate-200 rounded-3xl p-6 shadow-sm">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-sm font-bold text-slate-900"><i class="fa-solid fa-book-journal-whills text-slate-400 mr-2"></i> Ledger de Tarjetas de Regalo (Stored Value)</h3>
                <div class="flex space-x-2">
                    <span class="bg-slate-100 text-slate-600 text-xs font-bold px-3 py-1.5 rounded-lg cursor-pointer hover:bg-slate-200">Todas</span>
                    <span class="bg-emerald-50 text-emerald-600 text-xs font-bold px-3 py-1.5 rounded-lg cursor-pointer hover:bg-emerald-100">Recargas (In)</span>
                    <span class="bg-rose-50 text-rose-600 text-xs font-bold px-3 py-1.5 rounded-lg cursor-pointer hover:bg-rose-100">Consumos (Out)</span>
                </div>
            </div>
            
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="border-b border-slate-100">
                            <th class="py-3 px-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Fecha</th>
                            <th class="py-3 px-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">ID Tarjeta (Wallet)</th>
                            <th class="py-3 px-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Movimiento</th>
                            <th class="py-3 px-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Monto Neto</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b border-slate-50 hover:bg-slate-50/50 transition">
                            <td class="py-3 px-4 text-xs font-medium text-slate-600">Hoy, 10:42 AM</td>
                            <td class="py-3 px-4 text-xs font-mono font-bold text-slate-800">GC-8472-91A</td>
                            <td class="py-3 px-4"><span class="bg-emerald-50 text-emerald-600 text-[10px] font-bold px-2 py-1 rounded-md">Recarga de Saldo</span></td>
                            <td class="py-3 px-4 text-right font-black text-emerald-600">+$1,000.00</td>
                        </tr>
                        <tr class="border-b border-slate-50 hover:bg-slate-50/50 transition">
                            <td class="py-3 px-4 text-xs font-medium text-slate-600">Hoy, 09:15 AM</td>
                            <td class="py-3 px-4 text-xs font-mono font-bold text-slate-800">GC-1193-44B</td>
                            <td class="py-3 px-4"><span class="bg-rose-50 text-rose-600 text-[10px] font-bold px-2 py-1 rounded-md">Consumo en Tienda</span></td>
                            <td class="py-3 px-4 text-right font-black text-slate-900">-$245.00</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Modal Emitir Gift Card -->
        <div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm px-4" x-show="issueGiftCard" style="display: none;">
            <div @click.away="issueGiftCard = false" class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden border border-slate-200" x-show="issueGiftCard" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 transform scale-95" x-transition:enter-end="opacity-100 transform scale-100">
                <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 rounded-full bg-slate-900 text-white flex items-center justify-center">
                            <i class="fa-brands fa-apple text-lg"></i>
                        </div>
                        <div>
                            <h3 class="text-sm font-black text-slate-900">Emitir Tarjeta de Regalo</h3>
                            <p class="text-[10px] uppercase tracking-widest font-bold text-slate-500">Apple Wallet Stored Value</p>
                        </div>
                    </div>
                    <button @click="issueGiftCard = false" class="w-8 h-8 rounded-full hover:bg-slate-200 flex items-center justify-center text-slate-500 transition">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
                <div class="p-6 space-y-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Teléfono del Destinatario (SMS)</label>
                        <input type="tel" class="w-full bg-white border border-slate-200 text-slate-900 text-sm font-medium rounded-xl px-4 py-3 focus:outline-none focus:border-slate-900 focus:ring-1 focus:ring-slate-900 transition" placeholder="+52 55..." x-model="customerPhone">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Monto a Cargar (MXN)</label>
                        <div class="relative">
                            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-bold">$</span>
                            <input type="number" class="w-full bg-white border border-slate-200 text-slate-900 text-lg font-black rounded-xl pl-8 pr-4 py-3 focus:outline-none focus:border-slate-900 focus:ring-1 focus:ring-slate-900 transition" x-model="giftAmount">
                        </div>
                    </div>
                    <p class="text-xs text-slate-500 font-medium mt-2"><i class="fa-solid fa-circle-info text-slate-400 mr-1"></i> El cliente recibirá un enlace por SMS para guardar su tarjeta con el saldo exacto en Apple Wallet.</p>
                </div>
                <div class="p-4 bg-slate-50 border-t border-slate-100">
                    <button @click="issueGiftCard = false" class="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-3 rounded-xl transition shadow-md flex items-center justify-center">
                        <i class="fa-solid fa-paper-plane mr-2"></i> Emitir y Enviar SMS
                    </button>
                </div>
            </div>
        </div>

    </div>
</section>
"""

content = content.replace('<!-- TAB AUTOPILOT (FIDELITO AI) -->', bank_html + '\n<!-- TAB AUTOPILOT (FIDELITO AI) -->')

with open('index.html', 'w') as f:
    f.write(content)
print("Bank UI patched successfully")
