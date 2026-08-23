import re

with open('scanner.html', 'r') as f:
    content = f.read()

# 1. Add Apple VAS / NFC UI to the scanner screen
old_camera_ui = """<!-- Camera Viewport -->
                <div class="relative aspect-square w-full max-w-sm mx-auto bg-slate-900 rounded-3xl overflow-hidden shadow-2xl mb-6">"""

new_camera_ui = """
                <!-- Scan Mode Toggle -->
                <div class="flex justify-center mb-6">
                    <div class="bg-slate-200/50 p-1 rounded-2xl flex space-x-1">
                        <button class="px-6 py-2 rounded-xl text-sm font-bold transition shadow-sm" :class="scanMode === 'qr' ? 'bg-white text-slate-900' : 'text-slate-500 hover:text-slate-700'" @click="scanMode = 'qr'">
                            <i class="fa-solid fa-qrcode mr-2"></i>QR / Barras
                        </button>
                        <button class="px-6 py-2 rounded-xl text-sm font-bold transition shadow-sm flex items-center" :class="scanMode === 'nfc' ? 'bg-fidelio-600 text-white' : 'text-slate-500 hover:text-slate-700'" @click="scanMode = 'nfc'">
                            <i class="fa-brands fa-apple mr-2"></i>Apple VAS <span x-show="scanMode !== 'nfc'" class="ml-1.5 bg-fidelio-100 text-fidelio-600 px-1.5 py-0.5 rounded text-[8px] uppercase tracking-widest">NFC</span>
                        </button>
                    </div>
                </div>

                <!-- Camera Viewport (QR Mode) -->
                <div x-show="scanMode === 'qr'" class="relative aspect-square w-full max-w-sm mx-auto bg-slate-900 rounded-3xl overflow-hidden shadow-2xl mb-6">"""

content = content.replace(old_camera_ui, new_camera_ui)
content = content.replace('x-data="scannerApp()"', 'x-data="scannerApp()" x-init="$watch(\'scanMode\', val => { if(val===\'nfc\') triggerNFCSimulation(); })"')

# 2. Add NFC Mockup UI
nfc_ui = """
                <!-- NFC Apple VAS Viewport -->
                <div x-show="scanMode === 'nfc'" style="display:none;" class="relative aspect-square w-full max-w-sm mx-auto bg-slate-900 rounded-3xl overflow-hidden shadow-2xl mb-6 flex flex-col items-center justify-center">
                    <div class="absolute inset-0 bg-gradient-to-b from-fidelio-900/40 to-slate-900 z-0"></div>
                    
                    <div class="relative z-10 flex flex-col items-center">
                        <div class="w-24 h-24 rounded-full bg-slate-800/80 border border-slate-700 flex items-center justify-center mb-6 relative">
                            <!-- Radar ripples -->
                            <div class="absolute inset-0 rounded-full border-2 border-fidelio-500 animate-ping opacity-20"></div>
                            <div class="absolute inset-[-20px] rounded-full border border-fidelio-400 animate-ping opacity-10" style="animation-delay: 0.5s"></div>
                            
                            <i class="fa-solid fa-wifi text-4xl text-fidelio-400" style="transform: rotate(90deg);"></i>
                        </div>
                        <h3 class="text-white font-black text-xl mb-2">Acerca el iPhone</h3>
                        <p class="text-slate-400 text-sm font-medium text-center px-8">El cliente solo necesita acercar su teléfono. No es necesario abrir la cámara.</p>
                        
                        <div class="mt-8 flex items-center space-x-2 bg-slate-800/50 px-4 py-2 rounded-full border border-slate-700/50">
                            <i class="fa-brands fa-apple text-slate-300"></i>
                            <span class="text-[10px] font-bold text-slate-300 uppercase tracking-widest">Apple VAS Activo</span>
                        </div>
                    </div>
                </div>
"""

content = content.replace('<!-- Manual Entry Fallback -->', nfc_ui + '\n                <!-- Manual Entry Fallback -->')

# 3. Add JS logic for NFC toggle
js_logic = """
            return {
                scanMode: 'qr', // 'qr' or 'nfc'
                triggerNFCSimulation() {
                    // Simular que un cliente acerca su iPhone por NFC después de 3 segundos
                    if(this.scanMode === 'nfc' && this.view === 'scan') {
                        setTimeout(() => {
                            if(this.scanMode === 'nfc' && this.view === 'scan') {
                                this.manualCode = 'FID-827-392';
                                this.processCode();
                            }
                        }, 3500);
                    }
                },
"""

content = content.replace('return {', js_logic)

with open('scanner.html', 'w') as f:
    f.write(content)
print("Scanner patched successfully")
