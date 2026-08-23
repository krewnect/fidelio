const fs = require('fs');
let code = fs.readFileSync('app.js', 'utf8');

code = code.replace(
`                    backFields: [
                        { key: "promo", label: pushTitle || "Promociones", value: pushBody || "¡Visítanos pronto y acumula más sellos!", changeMessage: "%@" }
                    ]
                }
            }
        });`,
`                    backFields: [
                        { key: "promo", label: pushTitle || "Promociones", value: pushBody || "¡Visítanos pronto y acumula más sellos!", changeMessage: "%@" }
                    ]
                }
            }))
        });`
);

fs.writeFileSync('app.js', code);
