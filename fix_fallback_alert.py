import re

with open('merchant-public.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """            } catch (err) {
                Swal.fire('Error', err.message, 'error');
                btn.disabled = false;
                document.getElementById('btn-icon').style.display = 'inline-block';
                document.getElementById('btn-text').style.display = 'inline-block';
                document.getElementById('btn-loader').style.display = 'none';
            }"""

replacement = """            } catch (err) {
                console.error("Submit Error:", err);
                const msg = err.message || JSON.stringify(err);
                if (typeof Swal !== 'undefined') {
                    Swal.fire('Error', msg, 'error');
                } else {
                    alert('Error: ' + msg);
                }
                btn.disabled = false;
                document.getElementById('btn-icon').style.display = 'inline-block';
                document.getElementById('btn-text').style.display = 'inline-block';
                document.getElementById('btn-loader').style.display = 'none';
            }"""

text = text.replace(target, replacement)

with open('merchant-public.html', 'w', encoding='utf-8') as f:
    f.write(text)
