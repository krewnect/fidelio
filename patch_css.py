import re

with open('index.html', 'r') as f:
    content = f.read()

css_polish = """
        /* ==========================================================================
           FIDELIO $10M SIGNATURE POLISH (Apple Glass-Sheen + Fintech Typography)
           ========================================================================== */
        
        /* 1. Tipografía Suiza / Fintech: Alineación métrica perfecta y números tabulares */
        body, input, button, select, textarea {
            font-feature-settings: "cv02", "cv03", "cv04", "cv11", "tnum" 1 !important;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* 2. Apple Specular Inset & Layered Ambient Shadow (Luz física en tarjetas blancas) */
        .premium-white-card,
        .stat-card,
        .content-panel,
        .fidelio-card,
        .tab-content > div[class*="bg-white"],
        .tab-content > div[class*="bg-slate-50"] {
            background: #ffffff !important;
            border: 1px solid rgba(226, 232, 240, 0.8) !important; /* border-slate-200 */
            box-shadow: 
                inset 0 1px 0 0 rgba(255, 255, 255, 1),           /* Luz especular Apple */
                0 1px 3px 0 rgba(15, 23, 42, 0.03),               /* Sombra de contacto */
                0 8px 24px -4px rgba(124, 58, 237, 0.04) !important; /* Brillo ambiental morado */
            transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), 
                        box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                        border-color 0.22s ease !important;
        }
        
        .premium-white-card:hover,
        .stat-card:hover,
        .tab-content > div[class*="bg-white"]:hover {
            transform: translateY(-2px);
            border-color: rgba(196, 181, 253, 0.6) !important; /* Fidelio-300 soft ring */
            box-shadow: 
                inset 0 1px 0 0 rgba(255, 255, 255, 1),
                0 4px 6px -1px rgba(15, 23, 42, 0.04),
                0 20px 32px -8px rgba(124, 58, 237, 0.1) !important;
        }
        
        /* 3. Micro-interacción Háptica en Botones e Interactivos */
        button:active, 
        .btn:active, 
        .fidelio-btn-secondary:active,
        .action-card:active {
            transform: scale(0.982) !important;
            transition: transform 0.08s ease-out !important;
        }
        
        /* 4. Radar & Live Beacons: Pulso etéreo de IA */
        .animate-radar-ping {
            animation: fidelioRadarPulse 2.4s cubic-bezier(0, 0, 0.2, 1) infinite !important;
        }
        
        @keyframes fidelioRadarPulse {
            0% { transform: scale(0.95); opacity: 0.7; box-shadow: 0 0 0 0 rgba(124, 58, 237, 0.5); }
            70% { transform: scale(1.4); opacity: 0; box-shadow: 0 0 0 16px rgba(124, 58, 237, 0); }
            100% { transform: scale(1.4); opacity: 0; }
        }
"""

content = content.replace('</style>', css_polish + '\n    </style>')

with open('index.html', 'w') as f:
    f.write(content)
print("CSS patched successfully")
