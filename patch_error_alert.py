with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

error_script = """<script>
window.onerror = function(message, source, lineno, colno, error) {
    alert("JS ERROR:\\n" + message + "\\nLínea: " + lineno + "\\nArchivo: " + source);
    return false;
};
window.addEventListener('unhandledrejection', function(event) {
    alert("PROMISE ERROR:\\n" + event.reason);
});
</script>
</head>"""

if "window.onerror" not in html:
    html = html.replace("</head>", error_script)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected global error alert.")
else:
    print("Already injected.")
