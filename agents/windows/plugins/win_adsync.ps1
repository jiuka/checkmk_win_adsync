Write-Host '<<<win_adsync_scheduler:sep(0):encoding(cp437)>>>'
Get-ADSyncScheduler

Write-Host '<<<win_adsync_connector:sep(59):encoding(cp437)>>>'
Foreach ($conn in Get-ADSyncConnector) {
    Foreach ($profile in $conn.RunProfiles) {
        $lastRun = Get-ADSyncRunProfileResult -NumberRequested 2 -ConnectorId $conn.Identifier -RunProfileId $profile.Identifier `
            | Where-Object -Property IsRunComplete | Select-Object -Index 0

        if ($null -eq $lastRun) { continue; }

        Write-Host -NoNewline "$($conn.Name) $($profile.Name);"
        Write-Host -NoNewline "$($lastRun.Result);"
        Write-Host -NoNewline "$($($lastRun.EndDate - $lastRun.StartDate).TotalSeconds);"
        Write-Host "$($lastRun.EndDate);"
    }
}