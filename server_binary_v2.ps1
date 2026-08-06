$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:8081/")
$listener.Start()
Write-Host "Local web server for binary_v2.html running at http://localhost:8081/"
while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        $filePath = Join-Path $PSScriptRoot "binary_v2.html"
        if ($request.Url.AbsolutePath -eq "/" -or $request.Url.AbsolutePath -eq "/binary_v2.html") {
            if (Test-Path $filePath) {
                $bytes = [System.IO.File]::ReadAllBytes($filePath)
                $response.ContentType = "text/html; charset=utf-8"
                $response.ContentLength64 = $bytes.Length
                $response.OutputStream.Write($bytes, 0, $bytes.Length)
            } else {
                $response.StatusCode = 404
            }
        } else {
            $response.StatusCode = 404
        }
        $response.Close()
    } catch {
        # ignore context interruption errors on shutdown
    }
}
