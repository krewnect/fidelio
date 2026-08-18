const fs = require('fs');
let code = fs.readFileSync('app.js', 'utf8');

// The replacement for the second occurrence (app.post('/api/wallet/apple'))
code = code.replace(
`                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: customer.id
                }
            }
        }, certs);`,
`                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: customer.id
                }
            }))
        }, certs);`
);

// Check if there is a third occurrence
code = code.replace(
`                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: "Mi Código"
                }
            }
        });`,
`                barcode: {
                    format: "PKBarcodeFormatQR",
                    message: customer.id,
                    messageEncoding: "iso-8859-1",
                    altText: "Mi Código"
                }
            }))
        });`
);

fs.writeFileSync('app.js', code);
