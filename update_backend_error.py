import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_catch = """    } catch (error) {
        console.error('Error en Gemini Magic Builder:', error);
        res.status(500).json({ error: 'Error al generar estrategia con IA.' });
    }"""

good_catch = """    } catch (error) {
        console.error('Error en Gemini Magic Builder:', error);
        res.status(500).json({ error: `Fallo interno de IA: ${error.message}` });
    }"""

js = js.replace(bad_catch, good_catch)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
