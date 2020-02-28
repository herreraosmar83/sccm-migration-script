#
# Press 'F5' to run this script. Running this script will load the ConfigurationManager
# module for Windows PowerShell and will connect to the site.
#
# This script was auto-generated at '1/30/2020 11:18:27 AM'.

# Uncomment the line below if running in an environment where script signing is 
# required.
#Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Site configuration
$SiteCode = "CN1" # Site code 
$ProviderMachineName = "grunter.csun.edu" # SMS Provider machine name

# Customizations
$initParams = @{}
#$initParams.Add("Verbose", $true) # Uncomment this line to enable verbose logging
#$initParams.Add("ErrorAction", "Stop") # Uncomment this line to stop the script on any errors

# Do not change anything below this line

# Import the ConfigurationManager.psd1 module 
if((Get-Module ConfigurationManager) -eq $null) {
    Import-Module "$($ENV:SMS_ADMIN_UI_PATH)\..\ConfigurationManager.psd1" @initParams 
}

# Connect to the site's drive if it is not already present
if((Get-PSDrive -Name $SiteCode -PSProvider CMSite -ErrorAction SilentlyContinue) -eq $null) {
    New-PSDrive -Name $SiteCode -PSProvider CMSite -Root $ProviderMachineName @initParams
}

# Set the current location to be the site code.
Set-Location "$($SiteCode):\" @initParams



$computerInfo = invoke-cmquery -name "PPM Devices Export to AP " 
#create empty hashtable to store items
$table = @()
for ($i=0; $i -lt $computerInfo.count;$i++){
    $info = $computerInfo[$i].SMS_G_System_COMPUTER_SYSTEM
    $id = $computerInfo[$i].SMS_G_System_COMPUTER_SYSTEM_PRODUCT
    $ip = $computerInfo[$i].SMS_R_System
    #ps object to store each attribute into one
    $item = New-Object PSObject

    $item | Add-Member -MemberType NoteProperty -name "Name" -value $info.Name
    $item | Add-Member -MemberType NoteProperty -name "IdentifyingNumber" -value $id.IdentifyingNumber
    $item | Add-Member -MemberType NoteProperty -name "Model" -value $info.Model
    $item | Add-Member -MemberType NoteProperty -name "Manufacturer" -value $info.Manufacturer
    $item | Add-Member -MemberType NoteProperty -name "MacAddress" -value $ip.MACAddresses[0]
    $item | Add-Member -MemberType NoteProperty -name "GUID" -value $ip.SMBIOSGUID
    if($ip.IPAddresses -eq $null){
        $item | Add-Member -MemberType NoteProperty -name "IPAddress" -value $null
    }else{
        $item | Add-Member -MemberType NoteProperty -name "IPAddress" -value $ip.IPAddresses[0]
        }
    $table += $item
}
 $table | Export-Csv -Path "C:/outfile.csv" -NoTypeInformation

 

#$computerInfo = invoke-cmquery -name "PPM De3vices Export to AP " | Select-Object SMS_G_System_COMPUTER_SYSTEM.Name,SMS_G_System_COMPUTER_SYSTEM.Model,SMS_G_System_COMPUTER_SYSTEM.Manufacturer, SMS_G_System_COMPUTER_SYSTEM_PRODUCT.IndentifyingNumber,IPAddresses[0],SMS_R_System.MACAddresses[0],SMS_R_System.SMBIOSGUID
