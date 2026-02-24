param(
    [string]$RedisHost = "127.0.0.1",
    [int]$RedisPort = 6380
)

function Send-Command {
    param([string]$cmd)

    $client = New-Object System.Net.Sockets.TcpClient($RedisHost, $RedisPort)
    $stream = $client.GetStream()
    $writer = New-Object System.IO.StreamWriter($stream)

    $writer.WriteLine($cmd)
    $writer.Flush()

    Start-Sleep -Milliseconds 200

    $bytes = New-Object byte[] 4096
    $count = $stream.Read($bytes, 0, $bytes.Length)
    $response = [System.Text.Encoding]::UTF8.GetString($bytes, 0, $count)

    $writer.Close()
    $client.Close()

    return $response
}

Write-Host "Mini-Redis PowerShell Client" -ForegroundColor Green
Write-Host "Conectado em ${RedisHost}:${RedisPort}" -ForegroundColor Cyan
Write-Host "Digite 'sair' para encerrar`n"

while ($true) {
    $cmd = Read-Host "redis"
    if ($cmd -eq "sair") { break }
    $result = Send-Command $cmd
    Write-Host $result -ForegroundColor Yellow
}