Set-ExecutionPolicy -Scope Process -ExecutionPolicy Unrestricted -Force

$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

cls

Write-Output "Collecting counters..."
Write-Output "Press Ctrl+C to exit."

$counters = @("\Processor(_Total)\% Processor Time", 
"\LogicalDisk(_Total)\Disk Reads/sec", 
"\LogicalDisk(_Total)\Disk Writes/sec") 

Get-Counter -Counter $counters -SampleInterval 1 -MaxSamples 3600 | 
    Export-Counter -FileFormat csv -Path "sql-perfmon-log.csv" -Force