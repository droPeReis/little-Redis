param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 6380
)

function Send-Command {
    param([string]$cmd)

    $client = New-Object System.Net.Sockets.TcpClient($Host, $Port)
    $stream = $client.GetStream()
    $writer = New-Object System.IO.StreamWriter($stream)
    $reader = New-Object System.IO.StreamReader($stream)

    $writer.WriteLine($cmd)
    $writer.Flush()

    Start-Sleep -Milliseconds 100
    $response = $reader.ReadLine()

    $writer.Close()
    $client.Close()

    return $response
}

# Modo interativo
Write-Host "Mini-Redis PowerShell Client" -ForegroundColor Green
Write-Host "Conectado em ${Host}:${Port}" -ForegroundColor Cyan
Write-Host "Digite 'sair' para encerrar`n"

while ($true) {
    $input = Read-Host "redis"
    if ($input -eq "sair") { break }
    $result = Send-Command $input
    Write-Host $result -ForegroundColor Yellow
}